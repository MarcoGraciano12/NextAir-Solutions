"""
StreamInput controller for CRUD operations.

Author: Marco Graciano
Date: 2025-03-26

Handles database operations for StreamInput model.
"""

from Desktop.db import engine
from sqlalchemy.orm import Session
from logging import Logger, getLogger
from Desktop.models import StreamInput


class StreamInputController:
    """
    Controller for StreamInput CRUD operations.

    Manages database transactions for StreamInput entities.
    Each method creates and closes its own session.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize StreamInputController.

        :param logger: Logger instance for logging operations
        """
        self.__logger = logger or getLogger(self.__class__.__name__)

    def create(self, name: str, url: str, channel: int, sample_rate: int, block_size: int):
        """
        Create a new stream input configuration.

        :param name: Unique input name
        :param url: Input source URL
        :param channel: Audio channel number
        :param sample_rate: Audio sample rate in Hz
        :param block_size: Audio block size
        :return: Tuple (success: bool, result: StreamInput or error message)
        """
        try:
            with Session(engine) as session:
                # Check if name exists
                if session.query(StreamInput).filter_by(name=name).first():
                    return False, f"StreamInput already exists: {name}"

                stream_input = StreamInput(
                    name=name,
                    url=url,
                    channel=channel,
                    sample_rate=sample_rate,
                    block_size=block_size
                )
                session.add(stream_input)
                session.commit()
                session.refresh(stream_input)

                return True, stream_input

        except Exception as e:
            self.__logger.error(f"Error creating stream input: {e}")
            return False, "Error creating stream input"

    def get(self, stream_input_id: int):
        """
        Get stream input by ID.

        :param stream_input_id: StreamInput primary key
        :return: Tuple (success: bool, result: StreamInput or error message)
        """
        try:
            with Session(engine) as session:
                stream_input = session.query(StreamInput).filter_by(stream_input_id=stream_input_id).first()

                if not stream_input:
                    return False, f"StreamInput not found: {stream_input_id}"

            return True, stream_input

        except Exception as e:
            self.__logger.error(f"Error retrieving stream input: {e}")
            return False, "Error retrieving stream input"

    def get_all(self):
        """
        Get all stream inputs.

        :return: Tuple (success: bool, result: list of StreamInputs or error message)
        """
        try:
            with Session(engine) as session:
                stream_inputs = session.query(StreamInput).all()

                return True, stream_inputs

        except Exception as e:
            self.__logger.error(f"Error retrieving stream inputs: {e}")
            return False, "Error retrieving stream inputs"

    def get_by_name(self, name: str):
        """
        Get stream input by name.

        :param name: Input name to search
        :return: Tuple (success: bool, result: StreamInput or error message)
        """
        try:
            with Session(engine) as session:
                stream_input = session.query(StreamInput).filter_by(name=name).first()

                if not stream_input:
                    return False, f"StreamInput not found: {name}"

            return True, stream_input

        except Exception as e:
            self.__logger.error(f"Error searching stream input: {e}")
            return False, "Error searching stream input"

    def update(self, stream_input_id: int, **kwargs):
        """
        Update stream input configuration.

        :param stream_input_id: StreamInput primary key
        :param kwargs: Fields to update (name, url, channel, sample_rate, block_size)
        :return: Tuple (success: bool, result: StreamInput or error message)
        """
        try:
            with Session(engine) as session:
                # Check if stream input exists
                stream_input = session.query(StreamInput).filter_by(stream_input_id=stream_input_id).first()

                if not stream_input:
                    return False, f"StreamInput not found: {stream_input_id}"

                # If updating name, check it doesn't exist for another input
                if "name" in kwargs:
                    new_name = kwargs["name"]
                    exists = session.query(StreamInput).filter_by(name=new_name).first()

                    if exists and exists.stream_input_id != stream_input_id:
                        return False, f"StreamInput name already exists: {new_name}"

                # Update fields
                for key, value in kwargs.items():
                    if hasattr(stream_input, key):
                        setattr(stream_input, key, value)

                session.commit()
                session.refresh(stream_input)

                return True, stream_input

        except Exception as e:
            self.__logger.error(f"Error updating stream input: {e}")
            return False, "Error updating stream input"

    def delete(self, stream_input_id: int):
        """
        Delete stream input configuration.

        :param stream_input_id: StreamInput primary key
        :return: Tuple (success: bool, result: success message or error message)
        """
        try:
            with Session(engine) as session:
                # Check if stream input exists
                stream_input = session.query(StreamInput).filter_by(stream_input_id=stream_input_id).first()

                if not stream_input:
                    return False, f"StreamInput not found: {stream_input_id}"

                input_name = stream_input.name
                session.delete(stream_input)
                session.commit()

                return True, f"StreamInput deleted: {input_name}"

        except Exception as e:
            self.__logger.error(f"Error deleting stream input: {e}")
            return False, "Error deleting stream input"
