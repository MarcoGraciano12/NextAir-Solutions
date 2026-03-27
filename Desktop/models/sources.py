"""
Sources ORM model.

Author: Marco Graciano
Date: 2025-03-26

Represents recurring weekly schedule configuration for a stream.
"""

from db import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String, Time, ForeignKey


# Import Stream only for type checking to avoid circular imports
if TYPE_CHECKING:
    from .stream import Stream


class Sources(Base):
    """
    Weekly schedule configuration entity.

    Defines recurring time blocks by weekday for a stream.
    These configurations repeat weekly.

    :param source_id: Primary key
    :param stream_id: Foreign key to Stream
    :param start_time: Start time (hour of day)
    :param end_time: End time (hour of day)
    :param source: Source identifier (CADENA1, CADENA2, etc)
    :param weekday: Day of week (0=Monday, 6=Sunday)
    """

    __tablename__ = "sources"

    source_id = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(Integer, ForeignKey("streams.stream_id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    source = Column(String(100), nullable=False)
    weekday = Column(Integer, nullable=False)

    # Many-to-one relationship with Stream
    stream: Mapped["Stream"] = relationship(back_populates="sources")

    def to_dict(self):
        """
        Convert Sources to dictionary.

        :return: Dictionary with sources attributes
        """
        return {
            "source_id": self.source_id,
            "stream_id": self.stream_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "source": self.source,
            "weekday": self.weekday
        }
