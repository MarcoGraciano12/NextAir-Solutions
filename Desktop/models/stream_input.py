"""
StreamInput ORM model.

Author: Marco
Date: 2025-03-26
Represents an audio input source configuration.
"""

from Desktop.db import Base
from sqlalchemy import Column, Integer, String


class StreamInput(Base):
    """
    Audio input source configuration.

    Standalone entity with no relationships to other models.

    :param stream_input_id: Primary key
    :param name: Unique input name
    :param url: Input source URL
    :param channel: Audio channel number
    :param sample_rate: Audio sample rate in Hz
    :param block_size: Audio block size
    """

    __tablename__ = "stream_input"

    stream_input_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    url = Column(String(500), nullable=False)
    channel = Column(Integer, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    block_size = Column(Integer, nullable=False)
