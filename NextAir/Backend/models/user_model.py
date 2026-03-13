"""
User model definition.

Defines the UserModel class representing users in the system with support for
both admin and regular user roles. Includes helper methods for database operations
and user lookups.

Author: Marco Graciano
Date: January 13, 2026
"""

from db import db


class UserModel(db.Model):
    """
    User model for the system.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    @classmethod
    def find_by_username(cls, username):
        """
        Find a user by username.

        :param username: The username to search for
        :return: UserModel instance if found, None otherwise
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """
        Find a user by ID.

        :param _id: The user ID to search for
        :return: UserModel instance if found, None otherwise
        """
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        """
        Save the current user instance to the database.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current user instance from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()
