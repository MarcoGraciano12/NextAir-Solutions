"""
Broadcast ORM model.

Author: Marco
Date: 2025-03-26
Represents broadcast configuration for a stream.
"""

from Desktop.db import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String, ForeignKey


# Import Stream only for type checking to avoid circular imports
if TYPE_CHECKING:
    from .stream import Stream


class Broadcast(Base):
    """
    Broadcast configuration entity.

    One-to-one relationship with Stream.
    Contains streaming server connection details and audio settings.

    :param broadcast_id: Primary key
    :param stream_id: Foreign key to Stream (unique, one-to-one)
    :param name: Broadcast display name (unique)
    :param url: Streaming server URL (unique)
    :param user: Server authentication username
    :param password: Server authentication password
    :param channels: Audio channels count
    :param sample_rate: Audio sample rate in Hz
    :param block_size: Audio block size
    :param bitrate: Encoding bitrate
    """

    __tablename__ = "broadcast"

    broadcast_id = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(Integer, ForeignKey("streams.stream_id"), unique=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    user = Column(String(255), nullable=False)
    password = Column(String(200), nullable=False)
    channels = Column(Integer, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    block_size = Column(Integer, nullable=False)
    bitrate = Column(String(50), nullable=False)

    # One-to-one relationship with Stream
    stream: Mapped["Stream"] = relationship(back_populates="broadcast")