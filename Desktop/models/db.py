"""
Database configuration and connection management.

Author: Marco
Date: 2025-03-25
"""

from sqlalchemy import create_engine
from logging import Logger, getLogger
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class DatabaseManager:
    """
    Manages database connection and session lifecycle.
    """

    def __init__(self, connection_string: str, logger: Logger = None):
        """
        Initialize database manager.

        :param connection_string: PostgreSQL connection string
        :param logger: Logger instance
        """
        self.__logger = logger or getLogger(self.__class__.__name__)
        self.__engine = create_engine(connection_string, echo=False)
        self.__session_factory = sessionmaker(bind=self.__engine)

    def create_tables(self) -> bool:
        """
        Create all tables defined in models.

        :return: True if successful, False otherwise
        """
        try:
            Base.metadata.create_all(self.__engine)
            self.__logger.info("Tables created successfully")
            return True
        except Exception as e:
            self.__logger.error(f"Failed to create tables: {e}")
            return False

    def get_session(self):
        """
        Get a new database session.

        :return: SQLAlchemy session instance
        """
        return self.__session_factory()

    def close(self) -> bool:
        """
        Close database engine.

        :return: True if successful, False otherwise
        """
        try:
            self.__engine.dispose()
            self.__logger.info("Database connection closed")
            return True
        except Exception as e:
            self.__logger.error(f"Failed to close database: {e}")
            return False
