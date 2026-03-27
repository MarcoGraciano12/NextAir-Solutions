"""
Sources controller for CRUD operations.

Author: Marco
Date: 2025-03-26
Handles database operations for Sources model.
"""

from datetime import time
from db import engine
from sqlalchemy.orm import Session
from logging import Logger, getLogger
from models import Sources, Stream


class SourcesController:
    """
    Controller for Sources CRUD operations.

    Manages database transactions for Sources entities.
    Each method creates and closes its own session.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize SourcesController.

        :param logger: Logger instance for logging operations
        """
        self.__logger = logger or getLogger(self.__class__.__name__)

    def create(self, stream_id: int, start_time: time, end_time: time, source: str, weekday: int):
        """
        Create a new source configuration.

        :param stream_id: Foreign key to Stream
        :param start_time: Start time of day
        :param end_time: End time of day
        :param source: Source identifier
        :param weekday: Day of week
        :return: Tuple (success: bool, result: Sources or error message)
        """
        try:
            with Session(engine) as session:
                # Check if stream exists
                if not session.query(Stream).filter_by(stream_id=stream_id).first():
                    return False, f"Stream not found: {stream_id}"

                source_obj = Sources(
                    stream_id=stream_id,
                    start_time=start_time,
                    end_time=end_time,
                    source=source,
                    weekday=weekday
                )
                session.add(source_obj)
                session.commit()
                session.refresh(source_obj)

                return True, source_obj

        except Exception as e:
            self.__logger.error(f"Error creating source: {e}")
            return False, "Error creating source"

    def create_batch(self, stream_id: int, items: list):
        """
        Create multiple source configurations in bulk.

        :param stream_id: Stream primary key
        :param items: List of tuples (stream_id, start_time, end_time, source, weekday)
        :return: Tuple (success: bool, result: count or error message)
        """
        try:
            with Session(engine) as session:
                sources = [
                    Sources(
                        stream_id=stream_id,
                        start_time=start_time,
                        end_time=end_time,
                        source=source,
                        weekday=weekday
                    )
                    for start_time, end_time, source, weekday in items
                ]
                session.bulk_save_objects(sources)
                session.commit()

                return True, len(sources)

        except Exception as e:
            self.__logger.error(f"Error creating sources batch: {e}")
            return False, "Error creating sources batch"

    def get_by_stream_and_weekday(self, stream_id: int, weekday: int):
        """
        Get all source configurations for a stream on a specific weekday.

        :param stream_id: Stream primary key
        :param weekday: Day of week (0=Monday, 6=Sunday)
        :return: Tuple (success: bool, result: list of Sources or error message)
        """
        try:
            with Session(engine) as session:
                sources = session.query(Sources).filter_by(stream_id=stream_id, weekday=weekday).order_by(Sources.start_time).all()

                return True, sources

        except Exception as e:
            self.__logger.error(f"Error retrieving sources: {e}")
            return False, "Error retrieving sources"

    def delete_by_weekday(self, stream_id: int, weekday: int):
        """
        Delete all source configurations for a specific weekday.

        :param stream_id: Stream primary key
        :param weekday: Day of week (0=Monday, 6=Sunday)
        :return: Tuple (success: bool, result: deleted count or error message)
        """
        try:
            with Session(engine) as session:
                deleted_count = session.query(Sources).filter_by(stream_id=stream_id, weekday=weekday).delete()
                session.commit()

                return True, deleted_count

        except Exception as e:
            self.__logger.error(f"Error deleting sources: {e}")
            return False, "Error deleting sources"

    def replace_weekday(self, stream_id: int, weekday: int, new_sources: list):
        """
        Replace all source configurations for a specific weekday.

        Deletes existing sources and inserts new ones in a single transaction.

        :param stream_id: Stream primary key
        :param weekday: Day of week (0=Monday, 6=Sunday)
        :param new_sources: List of tuples (start_time, end_time, source)
        :return: Tuple (success: bool, result: count or error message)
        """
        try:
            with Session(engine) as session:
                # Delete existing sources for this weekday
                session.query(Sources).filter_by(stream_id=stream_id, weekday=weekday).delete()

                # Insert new sources
                sources = [
                    Sources(
                        stream_id=stream_id,
                        start_time=start_time,
                        end_time=end_time,
                        source=source,
                        weekday=weekday
                    )
                    for start_time, end_time, source in new_sources
                ]
                session.bulk_save_objects(sources)
                session.commit()

                return True, len(sources)

        except Exception as e:
            self.__logger.error(f"Error replacing sources: {e}")
            return False, "Error replacing sources"

    def get_all_by_stream(self, stream_id: int):
        """
        Get all source configurations for a stream (all weekdays).

        :param stream_id: Stream primary key
        :return: Tuple (success: bool, result: list of Sources or error message)
        """
        try:
            with Session(engine) as session:
                sources = session.query(Sources).filter_by(stream_id=stream_id).order_by(Sources.weekday, Sources.start_time).all()

                return True, sources

        except Exception as e:
            self.__logger.error(f"Error retrieving all sources: {e}")
            return False, "Error retrieving all sources"
