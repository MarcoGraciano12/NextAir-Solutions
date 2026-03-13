"""
User schemas for serialization and validation.

Marshmallow schemas for user data validation, serialization, and deserialization.
Includes schemas for user CRUD operations, authentication, and partial updates.

Author: Marco Graciano
Date: January 13, 2026
"""

from marshmallow import Schema, fields


class UserSchema(Schema):
    """
    Schema for user serialization and deserialization.
    """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    role = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserUpdateSchema(Schema):
    """
    Schema for partial user updates.
    """
    username = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    role = fields.Str()
    password = fields.Str(load_only=True)


class UserLoginSchema(Schema):
    """
    Schema for user login credentials.
    """
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
