"""
Application setup and initialization.

Author: Marco Graciano
Date: 2025-03-25
"""

import os
import logging
from dotenv import load_dotenv
from models import DatabaseManager


class Setup:
    """
    Handles application initialization and configuration.
    """

    def __init__(self):
        """Initialize setup manager."""
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__db_manager = None

    def initialize(self) -> bool:
        """
        Load environment variables and initialize database.

        :return: True if successful, False otherwise
        """
        if not load_dotenv():
            self.__logger.warning("No .env file found")

        try:
            connection_string = (
                f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            )

            self.__db_manager = DatabaseManager(connection_string)

            if not self.__db_manager.create_tables():
                self.__logger.error("Failed to create database tables")
                return False

            self.__logger.info("Setup completed successfully")
            return True
        except Exception as e:
            self.__logger.error(f"Setup initialization failed: {e}")
            return False

    @property
    def db_manager(self) -> DatabaseManager:
        """
        Get database manager instance.
        """
        return self.__db_manager


# Global instance
setup = Setup()
