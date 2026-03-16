"""
Flask application initialization and configuration.

Main application entry point that configures the Flask app, initializes extensions
(SQLAlchemy, Flask-Smorest, JWT), registers blueprints, and sets up JWT callbacks
for token validation and error handling.

Author: Marco Graciano
Date: January 13, 2026
"""

# Logs global configuration
from controller import setup

import os
import secrets
from db import db
from flask_cors import CORS
from flask_smorest import Api
from datetime import timedelta
from flask import Flask, jsonify
from models import BlocklistModel
from flask_jwt_extended import JWTManager
from controller.init_database import init_database


app = Flask(__name__)
CORS(app)

# API configuration
app.config["API_TITLE"] = "NextAir Solutions"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"

# Swagger UI configuration
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

# Initialize extensions
db.init_app(app)
api = Api(app)

# Set up the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or secrets.token_hex(32)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Check if a token has been revoked.

    :param jwt_header: JWT header
    :param jwt_payload: JWT payload containing claims
    :return: True if token is revoked, False otherwise
    """
    return BlocklistModel.is_jti_blocklisted(jwt_payload["jti"])


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """
    Callback for expired token errors.

    :param jwt_header: JWT header
    :param jwt_payload: JWT payload
    :return: JSON response with error message
    """
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Callback for invalid token errors.

    :param error: Error details
    :return: JSON response with error message
    """
    return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    Callback for missing token errors.

    :param error: Error details
    :return: JSON response with error message
    """
    return jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    """
    Callback for non-fresh token errors.

    :param jwt_header: JWT header
    :param jwt_payload: JWT payload
    :return: JSON response with error message
    """
    return jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """
    Callback for revoked token errors.

    :param jwt_header: JWT header
    :param jwt_payload: JWT payload
    :return: JSON response with error message
    """
    return jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401


with app.app_context():
    db.create_all()
    init_database(app)

    from resources import *

api.register_blueprint(day_blueprint)
api.register_blueprint(user_blueprint)
api.register_blueprint(block_blueprint)
api.register_blueprint(stream_blueprint)
api.register_blueprint(station_blueprint)
