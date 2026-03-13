"""
Author: Marco Graciano
Date: January 13, 2026

Custom decorators for authentication and authorization.
"""

from functools import wraps
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt


def _get_user_role():
    """
    Extract role from current JWT token.

    :return: User role from JWT claims
    """
    claims = get_jwt()
    return claims.get("role")


def _validate_admin_role(role):
    """
    Validate if the given role is admin.

    :param role: Role to validate
    :return: None (aborts if not admin)
    """
    if role != "admin":
        abort(403, message="Admin privileges required")


def admin_required(fn):
    """
    Decorator to require admin role for accessing endpoints.
    Combines JWT requirement with role validation.

    :param fn: Function to decorate
    :return: Decorated function that validates admin privileges
    """

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        role = _get_user_role()
        _validate_admin_role(role)
        return fn(*args, **kwargs)

    return wrapper
