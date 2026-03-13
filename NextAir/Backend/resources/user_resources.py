"""
User resource endpoints.

REST API resources for user management including CRUD operations, authentication
(login/logout), and token refresh. All user management endpoints are protected
and require admin privileges.

Author: Marco Graciano
Date: January 13, 2026
"""

from models import UserModel
from datetime import datetime
from models import BlocklistModel
from flask.views import MethodView
from controller import admin_required
from passlib.hash import pbkdf2_sha256
from flask_smorest import Blueprint, abort
from schemas import UserSchema, UserUpdateSchema, UserLoginSchema
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required


blp = Blueprint("Users", __name__, description="User management operations")


@blp.route("/users")
class UserCollection(MethodView):
    """
    Resource for user collection operations.
    """

    @blp.response(200, UserSchema(many=True))
    @admin_required
    def get(self):
        """
        Get all users.

        :return: List of all users
        """
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    @admin_required
    def post(self, user_data):
        """
        Create a new user.

        :param user_data: User data from request body
        :return: Created user
        """
        if UserModel.find_by_username(user_data["username"]):
            abort(400, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            name=user_data["name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        user.save_to_db()

        return user


@blp.route("/users/<int:user_id>")
class UserItem(MethodView):
    """
    Resource for individual user operations.
    """

    @blp.response(200, UserSchema)
    @admin_required
    def get(self, user_id):
        """
        Get a user by ID.

        :param user_id: User ID
        :return: User data
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    @admin_required
    def patch(self, user_data, user_id):
        """
        Update a user partially.

        :param user_data: Updated user data from request body
        :param user_id: User ID
        :return: Updated user data
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")

        # Update fields if present in user_data
        if "username" in user_data:
            user.username = user_data["username"]
        if "name" in user_data:
            user.name = user_data["name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "role" in user_data:
            user.role = user_data["role"]
        if "password" in user_data:
            user.password = pbkdf2_sha256.hash(user_data["password"])

        user.save_to_db()
        return user

    @blp.response(204)
    @admin_required
    def delete(self, user_id):
        """
        Delete a user by ID.

        :param user_id: User ID
        :return: None
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        user.delete_from_db()


@blp.route("/login")
class Login(MethodView):
    """
    Resource for user authentication.
    """

    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        """
        Authenticate user and return access token.

        :param login_data: Login credentials from request body
        :return: Access token and refresh token
        """
        user = UserModel.find_by_username(login_data["username"])

        if user and pbkdf2_sha256.verify(login_data["password"], user.password):
            access_token = create_access_token(
                identity=str(user.id),
                fresh=True,
                additional_claims={"role": user.role}
            )
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class Logout(MethodView):
    """
    Resource for revoking access tokens.
    """

    @jwt_required()
    def post(self):
        """
        Revoke the current access token.

        :return: Logout confirmation
        """
        jti = get_jwt()["jti"]
        exp = get_jwt()["exp"]

        expires_at = datetime.fromtimestamp(exp)

        token = BlocklistModel(jti=jti, expires_at=expires_at)
        token.save_to_db()

        return {"message": "Access token successfully revoked"}, 200


@blp.route("/logout-refresh")
class LogoutRefresh(MethodView):
    """
    Resource for revoking refresh tokens.
    """

    @jwt_required(refresh=True)
    def post(self):
        """
        Revoke the current refresh token.

        :return: Logout confirmation
        """
        jti = get_jwt()["jti"]
        exp = get_jwt()["exp"]

        expires_at = datetime.fromtimestamp(exp)

        token = BlocklistModel(jti=jti, expires_at=expires_at)
        token.save_to_db()

        return {"message": "Refresh token successfully revoked"}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    """
    Resource for refreshing access tokens.
    """

    @jwt_required(refresh=True)
    def post(self):
        """
        Get a new access token using a refresh token.

        :return: New access token
        """
        current_user_id = int(get_jwt_identity())
        user = UserModel.find_by_id(current_user_id)

        new_token = create_access_token(
            identity=str(current_user_id),
            fresh=False,
            additional_claims={"role": user.role}
        )
        return {"access_token": new_token}, 200
