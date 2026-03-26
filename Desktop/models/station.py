"""
Station ORM model.

Author: Marco
Date: 2025-03-26
Represents a radio station with associated streams.
"""

from Desktop.db import Base
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped


# Import Stream only for type checking to avoid circular imports
# At runtime this block is skipped, but IDEs and mypy can resolve types
if TYPE_CHECKING:
    from .stream import Stream


class Station(Base):
    """
    Radio station entity.

    :param station_id: Primary key
    :param station_name: Station display name (unique)
    :param files_path: File system path for station files
    """

    __tablename__ = "stations"

    station_id = Column(Integer, primary_key=True, autoincrement=True)
    station_name = Column(String(100), nullable=False, unique=True)
    files_path = Column(String(255), nullable=False)

    # One-to-many relationship: one station has multiple streams
    streams: Mapped[List["Stream"]] = relationship(back_populates="station", lazy=True, cascade="all, delete-orphan")
