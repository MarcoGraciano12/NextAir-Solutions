"""
Stream ORM model.

Author: Marco Graciano
Date: 2025-03-26

Represents an audio stream belonging to a station.
"""

from Desktop.db import Base
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String, ForeignKey


# Import Station only for type checking to avoid circular imports
if TYPE_CHECKING:
    from .station import Station
    from .broadcast import Broadcast


class Stream(Base):
    """
    Audio stream entity.

    :param stream_id: Primary key
    :param station_id: Foreign key to Station
    :param stream_name: Stream display name (unique)
    :param external_id: External system identifier
    """

    __tablename__ = "streams"

    stream_id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("stations.station_id"), nullable=False)
    stream_name = Column(String(100), nullable=False, unique=True)
    external_id = Column(Integer, nullable=False)

    # Many-to-one relationship: multiple streams belong to one station
    station: Mapped["Station"] = relationship(back_populates="streams")

    # One-to-one relationship: one stream has one broadcast configuration
    # CASCADE: deleting stream deletes its broadcast config
    broadcast: Mapped[Optional["Broadcast"]] = relationship(
        back_populates="stream",
        cascade="all, delete-orphan",
        uselist=False,  # One-to-one relationship
        lazy=False  # Always eager load
    )

    def to_dict(self):
        """
        Convert Stream to dictionary.

        :return: Dictionary with stream attributes only
        """
        return {
            "stream_id": self.stream_id,
            "station_id": self.station_id,
            "stream_name": self.stream_name,
            "external_id": self.external_id
        }
