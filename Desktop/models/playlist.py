"""
Playlist ORM model.

Author: Marco Graciano
Date: 2025-03-26

Represents daily programming schedule for a stream.
"""

from db import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey


# Import Stream only for type checking to avoid circular imports
if TYPE_CHECKING:
    from .stream import Stream


class Playlist(Base):
    """
    Daily programming schedule entity.

    Contains specific broadcast items for a stream on a given date.
    Multiple records per stream per day, organized by start_time.

    :param playlist_id: Primary key
    :param stream_id: Foreign key to Stream
    :param type_code: Content type (COR, SPO, PRG, etc)
    :param start_time: Start time (hour of day)
    :param end_time: End time (hour of day)
    :param item_code: Item identifier (nullable)
    :param source: Source identifier (nullable)
    :param spot_id: Spot identifier
    :param broadcast_day: Broadcast date
    """

    __tablename__ = "playlist"

    playlist_id = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(Integer, ForeignKey("streams.stream_id"), nullable=False)
    type_code = Column(String(10), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    item_code = Column(String(50), nullable=True)
    source = Column(String(255), nullable=True)
    spot_id = Column(Integer, nullable=False)
    broadcast_day = Column(Date, nullable=False)

    # Many-to-one relationship with Stream
    stream: Mapped["Stream"] = relationship(back_populates="playlists")

    def to_dict(self):
        """
        Convert Playlist to dictionary.

        :return: Dictionary with playlist attributes
        """
        return {
            "playlist_id": self.playlist_id,
            "stream_id": self.stream_id,
            "type_code": self.type_code,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "item_code": self.item_code,
            "source": self.source,
            "spot_id": self.spot_id,
            "broadcast_day": self.broadcast_day.isoformat() if self.broadcast_day else None
        }
