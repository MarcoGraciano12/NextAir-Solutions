"""
Stream input controller for audio broadcasting system.

Author: Marco Graciano
Date: March 22, 2026

Description: Manages CRUD operations for audio input streams with thread-safe access.
"""

from threading import Lock
from decoders import Decoder
from inputs import StreamInput
from subjects import StreamSubject
from models import StreamInputModel
from logging import Logger, getLogger


class StreamInputController:
    """
    Controller for managing audio input streams.
    Handles CRUD operations with thread-safe access to stream instances.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize stream inputs controller.

        :param logger: Logger instance
        :return: None
        """
        self.__inputs = {}
        self.__lock = Lock()
        self.__logger = logger or getLogger(self.__class__.__name__)

    def initialize(self):
        """
        Load existing inputs from database into memory on startup.

        :return: None
        """
        try:
            self.__logger.info("Initializing stream inputs from database")

            # Retrieve all stream input records
            models = StreamInputModel.get_all()

            # Create in-memory objects for each database record
            for model in models:
                decoder = Decoder(model.name, model.url, model.channel, model.sample_rate, model.block_size)
                stream_input = StreamInput(model.name, decoder)
                stream_subject = StreamSubject(stream_input)

                # Register stream subject
                self.__inputs[model.name] = stream_subject

            self.__logger.info(f"Loaded {len(models)} inputs from database")

        except Exception as error:
            self.__logger.error(f"Failed to initialize inputs: {error}")

    def create_input(self, name: str, url: str, channel: int, sample_rate: int, block_size: int):
        """
        Create and register a new audio input stream.

        :param name: Stream input name
        :param url: Audio source URL
        :param channel: Audio channel configuration
        :param sample_rate: Sample rate in Hz
        :param block_size: Audio block size in samples
        :return: StreamInputModel if created, None if already exists or error
        """
        try:
            # Validate name uniqueness
            if StreamInputModel.find_by_name(name):
                self.__logger.warning(f"Input name already exists: {name}")
                return None, "A stream input with that name already exists"

            # Validate URL uniqueness
            if StreamInputModel.find_by_url(url):
                self.__logger.warning(f"Input URL already exists: {url}")
                return None, "A stream input with that URL already exists"

            with self.__lock:
                # Check if input already exists in memory
                if name in self.__inputs:
                    self.__logger.warning(f"Input already in memory: {name}")
                    return None, "Stream input already exists"

                # Save to database
                stream_input_model = StreamInputModel(
                    name=name,
                    url=url,
                    channel=channel,
                    sample_rate=sample_rate,
                    block_size=block_size
                )
                stream_input_model.save_to_db()

                # Create stream components
                decoder = Decoder(name, url, channel, sample_rate, block_size)
                stream_input = StreamInput(name, decoder)
                stream_subject = StreamSubject(stream_input)

                # Register in memory
                self.__inputs[name] = stream_subject

            self.__logger.info(f"Input created: {name}")
            return stream_input_model, None

        except Exception as error:
            self.__logger.error(f"Error creating input: {error}")
            return None, f"Failed to create stream input: {str(error)}"

    def retrieve_input(self, stream_input_id: int):
        """
        Get a stream input from database by ID.

        :param stream_input_id: Stream input ID
        :return: Tuple (StreamInputModel, message) - model is None on error
        """
        # Query database for input
        stream_input = StreamInputModel.find_by_id(stream_input_id)

        if not stream_input:
            self.__logger.warning(f"Input not found with ID: {stream_input_id}")
            return None, "Stream input not found"

        return stream_input, None

    def delete_input(self, stream_input_id: int):
        """
        Delete a stream input and stop its operations.

        :param stream_input_id: Stream input ID
        :return: Tuple (StreamInputModel, message) - model is None on error
        """
        try:
            # Get input from database
            stream_input_model = StreamInputModel.find_by_id(stream_input_id)

            if not stream_input_model:
                self.__logger.warning(f"Input not found with ID: {stream_input_id}")
                return None, "Stream input not found"

            # Get stream subject from memory
            with self.__lock:
                stream_subject = self.__inputs.get(stream_input_model.name)

            # Stop stream if exists in memory
            if stream_subject:
                if not stream_subject.stop():
                    self.__logger.warning(f"Failed to stop input: {stream_input_model.name}")
                    # return None, "Failed to stop stream input"

                # Remove from memory after successful stop
                with self.__lock:
                    self.__inputs.pop(stream_input_model.name, None)

            # Delete from database
            stream_input_model.delete_from_db()

            self.__logger.info(f"Input deleted: {stream_input_model.name}")
            return stream_input_model, None

        except Exception as error:
            self.__logger.error(f"Error deleting input: {error}")
            return None, f"Failed to delete stream input: {str(error)}"

    def retrieve_all_inputs(self):
        """
        Get all stream inputs from database.

        :return: Tuple (list of StreamInputModel, message) - list is None on error
        """
        try:
            inputs = StreamInputModel.get_all()
            return inputs, None

        except Exception as error:
            self.__logger.error(f"Error reading inputs: {error}")
            return None, f"Failed to read stream inputs: {str(error)}"

    def get_inputs_status(self):
        """
        Get status of all stream inputs.

        :return: Tuple (list of status dicts, message) - list is None on error
        """
        try:
            # Get all stream subjects from memory
            with self.__lock:
                subjects = list(self.__inputs.values())

            # Build status list
            status_list = [
                {
                    "name": subject.stream_input.name,
                    "url": subject.stream_input.url,
                    "active": subject.is_alive
                }
                for subject in subjects
            ]

            return status_list, None

        except Exception as error:
            self.__logger.error(f"Error getting inputs status: {error}")
            return None, f"Failed to get inputs status: {str(error)}"

    def get_input(self, name: str):
        """
        Get a stream subject by name for internal use.

        :param name: Stream input name
        :return: StreamSubject if found, None otherwise
        """
        with self.__lock:
            return self.__inputs.get(name)
