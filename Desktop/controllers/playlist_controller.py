"""
Playlist controller for CRUD operations.

Author: Marco Graciano
Date: 2025-03-26

Handles database operations for Playlist model.
"""

from db import engine
from datetime import date, time
from sqlalchemy.orm import Session
from logging import Logger, getLogger
from models import Playlist, Stream
from sqlalchemy import extract


class PlaylistController:
    """
    Controller for Playlist CRUD operations.

    Manages database transactions for Playlist entities.
    Each method creates and closes its own session.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize PlaylistController.

        :param logger: Logger instance for logging operations
        """
        self.__logger = logger or getLogger(self.__class__.__name__)

    def create(self, stream_id: int, type_code: str, start_time: time, end_time: time, item_code: str, source: str, spot_id: int, broadcast_day: date):
        """
        Create a new playlist entry.

        :param stream_id: Foreign key to Stream
        :param type_code: Content type
        :param start_time: Start time of day
        :param end_time: End time of day
        :param item_code: Item identifier (can be empty string)
        :param source: Source identifier (can be empty string)
        :param spot_id: Spot identifier
        :param broadcast_day: Broadcast date
        :return: Tuple (success: bool, result: Playlist or error message)
        """
        try:
            with Session(engine) as session:
                # Check if stream exists
                if not session.query(Stream).filter_by(stream_id=stream_id).first():
                    return False, f"Stream not found: {stream_id}"

                playlist = Playlist(
                    stream_id=stream_id,
                    type_code=type_code,
                    start_time=start_time,
                    end_time=end_time,
                    item_code=item_code,
                    source=source,
                    spot_id=spot_id,
                    broadcast_day=broadcast_day
                )

                session.add(playlist)
                session.commit()
                session.refresh(playlist)

                return True, playlist

        except Exception as e:
            self.__logger.error(f"Error creating playlist entry: {e}")
            return False, "Error creating playlist entry"

    def create_batch(self, items: list):
        """
        Create multiple playlist entries in bulk.

        :param items: List of tuples
        :return: Tuple (success: bool, result: count or error message)
        """
        try:
            with Session(engine) as session:
                playlists = []
                for item in items:
                    # Unpack tuple
                    stream_id, type_code, start_time, end_time, item_code, source, spot_id, broadcast_day = item

                    playlist = Playlist(
                        stream_id=stream_id,
                        type_code=type_code,
                        start_time=start_time,
                        end_time=end_time,
                        item_code=item_code,
                        source=source,
                        spot_id=spot_id,
                        broadcast_day=broadcast_day
                    )
                    playlists.append(playlist)

                session.bulk_save_objects(playlists)
                session.commit()

                return True, len(playlists)

        except Exception as e:
            self.__logger.error(f"Error creating playlist batch: {e}")
            return False, "Error creating playlist batch"

    def get_by_stream_and_date(self, stream_id: int, broadcast_day: date):
        """
        Get all playlist entries for a stream on a specific date.

        :param stream_id: Stream primary key
        :param broadcast_day: Broadcast date
        :return: Tuple (success: bool, result: list of Playlists or error message)
        """
        try:
            with Session(engine) as session:
                playlists = session.query(Playlist).filter_by(
                    stream_id=stream_id,
                    broadcast_day=broadcast_day
                ).order_by(Playlist.start_time).all()

                return True, playlists

        except Exception as e:
            self.__logger.error(f"Error retrieving playlist entries: {e}")
            return False, "Error retrieving playlist entries"

    def get_by_stream_date_hour(self, stream_id: int, broadcast_day: date, hour: int):
        """
        Get playlist entries for a specific hour.

        :param stream_id: Stream primary key
        :param broadcast_day: Broadcast date
        :param hour: Hour of day (0-23)
        :return: Tuple (success: bool, result: list of Playlists or error message)
        """
        try:
            with Session(engine) as session:

                playlists = session.query(Playlist).filter_by(
                    stream_id=stream_id,
                    broadcast_day=broadcast_day
                ).filter(
                    extract('hour', Playlist.start_time) == hour
                ).order_by(Playlist.start_time).all()

                return True, playlists

        except Exception as e:
            self.__logger.error(f"Error retrieving playlist entries by hour: {e}")
            return False, "Error retrieving playlist entries by hour"

    def delete_by_hour(self, stream_id: int, broadcast_day: date, hour: int):
        """
        Delete all playlist entries for a specific hour.

        :param stream_id: Stream primary key
        :param broadcast_day: Broadcast date
        :param hour: Hour of day (0-23)
        :return: Tuple (success: bool, result: deleted count or error message)
        """
        try:
            with Session(engine) as session:

                deleted_count = session.query(Playlist).filter_by(
                    stream_id=stream_id,
                    broadcast_day=broadcast_day
                ).filter(
                    extract('hour', Playlist.start_time) == hour
                ).delete()

                session.commit()

                return True, deleted_count

        except Exception as e:
            self.__logger.error(f"Error deleting playlist entries: {e}")
            return False, "Error deleting playlist entries"

    def replace_hour(self, stream_id: int, broadcast_day: date, hour: int, new_items: list):
        """
        Replace all playlist entries for a specific hour.

        Deletes existing entries and inserts new ones in a single transaction.

        :param stream_id: Stream primary key
        :param broadcast_day: Broadcast date
        :param hour: Hour of day (0-23)
        :param new_items: List of tuples (type, start_time, end_time, item_code, source, spot_id)
        :return: Tuple (success: bool, result: count or error message)
        """
        try:
            with Session(engine) as session:

                # Step 1: Delete existing entries for this hour
                session.query(Playlist).filter_by(
                    stream_id=stream_id,
                    broadcast_day=broadcast_day
                ).filter(
                    extract('hour', Playlist.start_time) == hour
                ).delete()

                # Step 2: Insert new entries
                playlists = []
                for item in new_items:
                    # Unpack tuple: (type, start_time, end_time, item_code, source, spot_id)
                    type_code, start_time, end_time, item_code, source, spot_id = item

                    playlist = Playlist(
                        stream_id=stream_id,
                        type=type_code,
                        start_time=start_time,
                        end_time=end_time,
                        item_code=item_code,
                        source=source,
                        spot_id=spot_id,
                        broadcast_day=broadcast_day
                    )
                    playlists.append(playlist)

                session.bulk_save_objects(playlists)
                session.commit()

                return True, len(playlists)

        except Exception as e:
            self.__logger.error(f"Error replacing playlist entries: {e}")
            return False, "Error replacing playlist entries"
