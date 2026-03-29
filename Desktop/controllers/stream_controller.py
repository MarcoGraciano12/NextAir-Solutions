"""
Stream controller for CRUD operations.

Author: Marco
Date: 2025-03-26
Handles database operations for Stream model.
"""

from db import engine
from sqlalchemy.orm import Session
from logging import Logger, getLogger
from models import Stream, Station


class StreamController:
    """
    Controller for Stream CRUD operations.

    Manages database transactions for Stream entities.
    Each method creates and closes its own session.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize StreamController.

        :param logger: Logger instance for logging operations
        """
        self.__logger = logger or getLogger(self.__class__.__name__)

    def create(self, station_id: int, stream_name: str, external_id: int):
        """
        Create a new stream for a station.

        :param station_id: Foreign key to Station
        :param stream_name: Unique stream name
        :param external_id: External system identifier
        :return: Tuple (success: bool, result: Stream or error message)
        """
        try:
            with Session(engine) as session:
                # Check if station exists
                station_exists = session.query(Station).filter_by(station_id=station_id).first()

                if not station_exists:
                    return False, f"Station not found: {station_id}"

                # Check if stream name already exists
                exists = session.query(Stream).filter_by(stream_name=stream_name).first()

                if exists:
                    return False, f"Stream already exists: {stream_name}"

                stream = Stream(station_id=station_id, stream_name=stream_name, external_id=external_id)

                session.add(stream)
                session.commit()
                session.refresh(stream)

                return True, stream

        except Exception as e:
            self.__logger.error(f"Error creating stream: {e}")
            return False, "Error creating stream"

    def get(self, stream_id: int):
        """
        Get stream by ID.

        :param stream_id: Stream primary key
        :return: Tuple (success: bool, result: Stream or error message)
        """
        try:
            with Session(engine) as session:
                stream = session.query(Stream).filter_by(stream_id=stream_id).first()

                if not stream:
                    return False, f"Stream not found: {stream_id}"

                return True, stream

        except Exception as e:
            self.__logger.error(f"Error retrieving stream: {e}")
            return False, "Error retrieving stream"

    def get_all(self):
        """
        Get all streams.

        :return: Tuple (success: bool, result: list of Streams or error message)
        """
        try:
            with Session(engine) as session:
                streams = session.query(Stream).all()
                return streams

        except Exception as e:
            self.__logger.error(f"Error retrieving streams: {e}")
            return None

    def get_by_station(self, station_id: int):
        """
        Get all streams for a specific station.

        :param station_id: Station primary key
        :return: Tuple (success: bool, result: list of Streams or error message)
        """
        try:
            with Session(engine) as session:
                streams = session.query(Stream).filter_by(station_id=station_id).all()
                return True, streams

        except Exception as e:
            self.__logger.error(f"Error retrieving streams for station: {e}")
            return False, "Error retrieving streams for station"

    def get_by_name(self, stream_name: str):
        """
        Get stream by name.

        :param stream_name: Stream name to search
        :return: Tuple (success: bool, result: Stream or error message)
        """
        try:
            with Session(engine) as session:
                stream = session.query(Stream).filter_by(stream_name=stream_name).first()

                if not stream:
                    return False, f"Stream not found: {stream_name}"

                return True, stream

        except Exception as e:
            self.__logger.error(f"Error searching stream: {e}")
            return False, "Error searching stream"

    def update(self, stream_id: int, **kwargs):
        """
        Update stream attributes.

        :param stream_id: Stream primary key
        :param kwargs: Fields to update (station_id, stream_name, external_id)
        :return: Tuple (success: bool, result: Stream or error message)
        """
        try:
            with Session(engine) as session:
                # Check if stream exists
                stream = session.query(Stream).filter_by(stream_id=stream_id).first()

                if not stream:
                    return False, f"Stream not found: {stream_id}"

                # If updating station_id, check station exists
                if "station_id" in kwargs:
                    new_station_id = kwargs["station_id"]
                    station_exists = session.query(Station).filter_by(station_id=new_station_id).first()

                    if not station_exists:
                        return False, f"Station not found: {new_station_id}"

                # If updating name, check it doesn't exist for another stream
                if "stream_name" in kwargs:
                    new_name = kwargs["stream_name"]
                    exists = session.query(Stream).filter_by(stream_name=new_name).first()

                    if exists and exists.stream_id != stream_id:
                        return False, f"Stream name already exists: {new_name}"

                # Update fields
                for key, value in kwargs.items():
                    if hasattr(stream, key):
                        setattr(stream, key, value)

                session.commit()
                session.refresh(stream)

                return True, stream

        except Exception as e:
            self.__logger.error(f"Error updating stream: {e}")
            return False, "Error updating stream"

    def delete(self, stream_name: str):
        """
        Delete stream by name.

        :param stream_name: Stream name to delete
        :return: Tuple (success: bool, result: success message or error message)
        """
        try:
            with Session(engine) as session:
                stream = session.query(Stream).filter_by(stream_name=stream_name).first()

                if not stream:
                    return False, f"Stream not found: {stream_name}"

                session.delete(stream)
                session.commit()

                return True, f"Stream deleted: {stream_name}"

        except Exception as e:
            self.__logger.error(f"Error deleting stream {stream_name}: {e}")
            return False, "Error deleting stream"
