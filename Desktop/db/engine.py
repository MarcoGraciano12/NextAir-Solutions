"""
Database engine and ORM base configuration.

Author: Marco Graciano
Date: 2025-03-26

Initializes the SQLAlchemy engine and declarative base for ORM models.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from os import getenv, makedirs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

# Build PostgreSQL connection URL
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
makedirs("instance", exist_ok=True)
DATABASE_URL = "sqlite:///instance/database.db"

# Create engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Maximum permanent connections
    max_overflow=10,  # Extra temporary connections when pool is full
    pool_pre_ping=True  # Validate connection before use
)

# Base class for all ORM models
Base = declarative_base()


def init_db():
    """
    Initialize database tables.

    Creates all tables defined in ORM models if they don't exist.
    Imports all models internally to avoid exposing them to the view layer.

    :return: True if successful, False otherwise
    """
    try:
        Base.metadata.create_all(bind=engine)
        return True

    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
