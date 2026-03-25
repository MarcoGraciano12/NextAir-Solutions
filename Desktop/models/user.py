"""
User model definition.

Defines the UserModel class representing users in the system with support for
both admin and regular user roles. Includes helper methods for database operations
and user lookups.

Author: Marco Graciano
Date: January 13, 2026
"""

from .db import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    """
    User model for authentication and authorization
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    @classmethod
    def find_by_username(cls, session, username: str):
        """
        Find a user by username.

        :param session: Database session
        :param username: Username to search
        :return: User instance if found, None otherwise
        """
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, session, user_id: int):
        """
        Find a user by ID.

        :param session: Database session
        :param user_id: User ID to search
        :return: User instance if found, None otherwise
        """
        return session.query(cls).filter_by(id=user_id).first()

    def save_to_db(self, session) -> bool:
        """
        Save the current user instance to the database.

        :param session: Database session
        :return: True if successful, False otherwise
        """
        try:
            session.add(self)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    def delete_from_db(self, session) -> bool:
        """
        Delete the current user instance from the database.

        :param session: Database session
        :return: True if successful, False otherwise
        """
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
