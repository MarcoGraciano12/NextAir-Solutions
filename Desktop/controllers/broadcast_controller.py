"""
Broadcast controller for CRUD operations.

Author: Marco Graciano
Date: 2025-03-26

Handles database operations for Broadcast model.
"""

from Desktop.db import engine
from sqlalchemy.orm import Session
from logging import Logger, getLogger
from Desktop.models import Broadcast, Stream


class BroadcastController:
    """
    Controller for Broadcast CRUD operations.

    Manages database transactions for Broadcast entities.
    Each method creates and closes its own session.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize BroadcastController.

        :param logger: Logger instance for logging operations
        """
        self.__logger = logger or getLogger(self.__class__.__name__)

    def create(self, stream_id: int, name: str, url: str, user: str, password: str, channels: int, sample_rate: int, block_size: int, bitrate: str):
        """
        Create a new broadcast configuration.

        :param stream_id: Foreign key to Stream (one-to-one)
        :param name: Unique broadcast name
        :param url: Unique streaming server URL
        :param user: Server authentication username
        :param password: Server authentication password
        :param channels: Audio channels count
        :param sample_rate: Audio sample rate in Hz
        :param block_size: Audio block size
        :param bitrate: Encoding bitrate
        :return: Tuple (success: bool, result: Broadcast or error message)
        """
        try:
            with Session(engine) as session:
                # Check if stream exists
                if not session.query(Stream).filter_by(stream_id=stream_id).first():
                    return False, f"Stream not found: {stream_id}"

                # Check if stream already has broadcast
                if session.query(Broadcast).filter_by(stream_id=stream_id).first():
                    return False, f"Stream {stream_id} already has broadcast configuration"

                # Check if name already exists
                if session.query(Broadcast).filter_by(name=name).first():
                    return False, f"Broadcast name already exists: {name}"

                # Check if URL already exists
                if session.query(Broadcast).filter_by(url=url).first():
                    return False, f"Broadcast URL already exists: {url}"

                broadcast = Broadcast(
                    stream_id=stream_id,
                    name=name,
                    url=url,
                    user=user,
                    password=password,
                    channels=channels,
                    sample_rate=sample_rate,
                    block_size=block_size,
                    bitrate=bitrate
                )
                session.add(broadcast)
                session.commit()
                session.refresh(broadcast)

                return True, broadcast

        except Exception as e:
            self.__logger.error(f"Error creating broadcast: {e}")
            return False, "Error creating broadcast"

    def get(self, broadcast_id: int):
        """
        Get broadcast by ID.

        :param broadcast_id: Broadcast primary key
        :return: Tuple (success: bool, result: Broadcast or error message)
        """
        try:
            with Session(engine) as session:
                broadcast = session.query(Broadcast).filter_by(broadcast_id=broadcast_id).first()

                if not broadcast:
                    return False, f"Broadcast not found: {broadcast_id}"

                return True, broadcast

        except Exception as e:
            self.__logger.error(f"Error retrieving broadcast: {e}")
            return False, "Error retrieving broadcast"

    def get_by_stream(self, stream_id: int):
        """
        Get broadcast configuration for a specific stream.

        :param stream_id: Stream primary key
        :return: Tuple (success: bool, result: Broadcast or error message)
        """
        try:
            with Session(engine) as session:
                broadcast = session.query(Broadcast).filter_by(stream_id=stream_id).first()

                if not broadcast:
                    return False, f"Broadcast not found for stream: {stream_id}"

                return True, broadcast

        except Exception as e:
            self.__logger.error(f"Error retrieving broadcast for stream: {e}")
            return False, "Error retrieving broadcast for stream"

    def get_by_name(self, name: str):
        """
        Get broadcast by name.

        :param name: Broadcast name to search
        :return: Tuple (success: bool, result: Broadcast or error message)
        """
        try:
            with Session(engine) as session:
                broadcast = session.query(Broadcast).filter_by(name=name).first()

                if not broadcast:
                    return False, f"Broadcast not found: {name}"

                return True, broadcast

        except Exception as e:
            self.__logger.error(f"Error searching broadcast: {e}")
            return False, "Error searching broadcast"

    def get_all(self):
        """
        Get all broadcast configurations.

        :return: Tuple (success: bool, result: list of Broadcasts or error message)
        """
        try:
            with Session(engine) as session:
                broadcasts = session.query(Broadcast).all()

                return True, broadcasts

        except Exception as e:
            self.__logger.error(f"Error retrieving broadcasts: {e}")
            return False, "Error retrieving broadcasts"

    def update(self, broadcast_id: int, **kwargs):
        """
        Update broadcast configuration.

        :param broadcast_id: Broadcast primary key
        :param kwargs: Fields to update (stream_id, name, url, user, password, channels, sample_rate, block_size, bitrate)
        :return: Tuple (success: bool, result: Broadcast or error message)
        """
        try:
            with Session(engine) as session:
                # Check if broadcast exists
                broadcast = session.query(Broadcast).filter_by(broadcast_id=broadcast_id).first()

                if not broadcast:
                    return False, f"Broadcast not found: {broadcast_id}"

                # If updating stream_id, check new stream exists and doesn't have broadcast
                if "stream_id" in kwargs:
                    new_stream_id = kwargs["stream_id"]

                    if not session.query(Stream).filter_by(stream_id=new_stream_id).first():
                        return False, f"Stream not found: {new_stream_id}"

                    # Check if new stream already has broadcast (excluding current)
                    stream_broadcast = session.query(Broadcast).filter_by(stream_id=new_stream_id).first()

                    if stream_broadcast and stream_broadcast.broadcast_id != broadcast_id:
                        return False, f"Stream {new_stream_id} already has broadcast configuration"

                # If updating name, check it doesn't exist for another broadcast
                if "name" in kwargs:
                    new_name = kwargs["name"]
                    exists = session.query(Broadcast).filter_by(name=new_name).first()

                    if exists and exists.broadcast_id != broadcast_id:
                        return False, f"Broadcast name already exists: {new_name}"

                # If updating URL, check it doesn't exist for another broadcast
                if "url" in kwargs:
                    new_url = kwargs["url"]
                    exists = session.query(Broadcast).filter_by(url=new_url).first()

                    if exists and exists.broadcast_id != broadcast_id:
                        return False, f"Broadcast URL already exists: {new_url}"

                # Update fields
                for key, value in kwargs.items():
                    if hasattr(broadcast, key):
                        setattr(broadcast, key, value)

                session.commit()
                session.refresh(broadcast)

                return True, broadcast

        except Exception as e:
            self.__logger.error(f"Error updating broadcast: {e}")
            return False, "Error updating broadcast"

    def delete(self, broadcast_id: int):
        """
        Delete broadcast configuration.

        :param broadcast_id: Broadcast primary key
        :return: Tuple (success: bool, result: success message or error message)
        """
        try:
            with Session(engine) as session:
                # Check if broadcast exists
                broadcast = session.query(Broadcast).filter_by(broadcast_id=broadcast_id).first()

                if not broadcast:
                    return False, f"Broadcast not found: {broadcast_id}"

                broadcast_name = broadcast.name
                session.delete(broadcast)
                session.commit()

                return True, f"Broadcast deleted: {broadcast_name}"

        except Exception as e:
            self.__logger.error(f"Error deleting broadcast: {e}")
            return False,f"Error deleting broadcast"
