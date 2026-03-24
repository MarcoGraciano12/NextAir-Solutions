"""
Station management for streaming system.

Author: Marco Graciano
Date: March 20, 2026

Description: Station object that manages multiple audio streams.
"""
from pyexpat import ErrorString

from models import StreamModel
from threading import Lock
from .stream import Stream
from logging import Logger, getLogger


class Station:
    """
    Radio station managing multiple audio streams.
    """

    def __init__(self, station_name: str, files_path: str, stream_input_controller, logger: Logger = None, **kwargs):
        """
        Initialize station instance.

        :param station_name: Station name
        :param files_path: Path to audio files directory
        :param stream_input_controller: Stream inputs controller reference
        :param logger: Logger instance
        :return: None
        """
        self.__streams = {}
        self.__lock = Lock()
        self.__files_path = files_path
        self.__station_name = station_name
        self.__stream_input_controller = stream_input_controller
        self.__logger = logger or getLogger(self.__station_name)

    @property
    def station_name(self) -> str:
        """
        Get station name.
        """
        return self.__station_name

    @station_name.setter
    def station_name(self, value: str):
        """
        Set station name.

        :param value: New station name
        """
        self.__station_name = value

    @property
    def files_path(self) -> str:
        """
        Get files path.
        """
        return self.__files_path

    @files_path.setter
    def files_path(self, value: str):
        """
        Set files path.

        :param value: New files path
        """
        self.__files_path = value

    def __str__(self) -> str:
        """
        String representation of station.

        :return: Formatted string with station attributes
        """
        return f"station_name: {self.__station_name}, files_path: {self.__files_path}"

    # ==================================================================================================================
    # STREAMS
    # ==================================================================================================================

    def initialize(self, station_id: int):
        """
        Load existing streams from database into memory.

        :param station_id: Station ID
        :return: None
        """
        try:
            self.__logger.info("Initializing streams from database")

            # Retrieve all stream records for this station
            models = StreamModel.find_by_station_id(station_id)

            # Create in-memory objects for each database record
            for model in models:
                stream = Stream(model.stream_name, model.external_id)

                # Register stream
                self.__streams[model.stream_name] = stream

            self.__logger.info(f"Loaded {len(models)} streams from database")

        except Exception as error:
            self.__logger.error(f"Failed to initialize streams: {error}")

    def create_stream(self, station_id: int, **kwargs):
        """
        Create a new stream for this station.

        :param station_id: Station ID
        :param kwargs: Stream configuration parameters
        :return: Tuple (StreamModel, message) - model is None on error
        """
        try:
            stream_name = kwargs.get("stream_name")
            external_id = kwargs.get("external_id")

            # Validate name uniqueness
            if StreamModel.find_by_name(stream_name):
                self.__logger.warning(f"Stream name already exists: {stream_name}")
                return None, "A stream with that name already exists"

            # Validate external_id uniqueness
            if StreamModel.find_by_external_id(external_id):
                self.__logger.warning(f"Stream external_id already exists: {external_id}")
                return None, "A stream with that external ID already exists"

            with self.__lock:
                # Check if stream already exists in memory
                if stream_name in self.__streams:
                    self.__logger.warning(f"Stream already in memory: {stream_name}")
                    return None, "Stream already exists"

                # Save to database
                stream_model = StreamModel(station_id=station_id, stream_name=stream_name, external_id=external_id)
                stream_model.save_to_db()

                # Create stream object
                self.__streams[stream_name] = Stream(stream_name, external_id)

            self.__logger.info(f"Stream created: {stream_name}")
            return stream_model, None

        except Exception as error:
            self.__logger.error(f"Error creating stream: {error}")
            return None, f"Failed to create stream: {str(error)}"

    def delete_stream(self, stream_name: str):
        """
        Stop and remove stream from memory.

        :param stream_name: Stream name
        :return: True if deleted successfully, False otherwise
        """
        # Get stream from memory
        with self.__lock:
            stream = self.__streams.get(stream_name)

        if not stream:
            self.__logger.info(f"Stream not in memory: {stream_name}")
            return None, "Stream not found"

        # Stop stream operations
        if not stream.stop():
            self.__logger.error(f"Failed to stop stream: {stream_name}")
            return None, "Failed to stop stream"

        # Remove from memory after successful stop
        with self.__lock:
            self.__streams.pop(stream_name, None)

        self.__logger.info(f"Stream deleted from memory: {stream_name}")
        return self.delete_stream_by_name(stream_name)

    @staticmethod
    def find_stream_by_name(stream_name: str):
        """
        Get a stream by name.

        :param stream_name: Stream name
        :return: Tuple (StreamModel, message) - model is None on error
        """
        return StreamModel.find_by_name(stream_name)

    @staticmethod
    def get_all_streams():
        """
        Get all streams from database.

        :return: Tuple (list of StreamModel, message) - list is None on error
        """
        return StreamModel.get_all()

    @staticmethod
    def get_streams_by_station_id(station_id: int):
        """
        Get all streams for a station by ID.

        :param station_id: Station ID
        :return: Tuple (list of StreamModel, message) - list is None on error
        """
        return StreamModel.find_by_station_id(station_id)

    @staticmethod
    def delete_stream_by_name(stream_name: str):
        """
        Delete a stream by name.

        :param stream_name: Stream name
        :return: Tuple (StreamModel, message) - model is None on error
        """
        stream_model = StreamModel.find_by_name(stream_name)

        if not stream_model:
            return None, "Stream not found"

        stream_model.delete_from_db()
        return stream_model, None

    # ==================================================================================================================
    # SINGLE TRANSMISSION
    # ==================================================================================================================

    def start(self, stream_name: str):
        """
        Start a station's transmission

        :param stream_name: name of the stream
        :return: tuple
        """
        with self.__lock:
            stream = self.__streams.get(stream_name, None)

        if not stream:
            self.__logger.info(f"Stream {stream_name} not found in memory, trying on db")
            stream_model = StreamModel.find_by_name(stream_name)

            if not stream_model:
                self.__logger.warning(f"Stream {stream_name} not found in db")
                return False, "Stream not found in db"

            stream = Stream(stream_model.stream_name, stream_model.external_id)

            with self.__lock:
                if stream_name not in self.__streams:
                    self.__streams[stream_name] = stream
                    self.__logger.info(f"Stream {stream_name} added to memory")
                else:
                    stream = self.__streams[stream_name]
                    self.__logger.info(f"Stream {stream_name} already in memory (added by another thread)")

        return stream.start()

    def stop(self, stream_name: str):
        """
        Stop a station's transmission

        :param stream_name: name of the stream
        :return: tuple
        """
        with self.__lock:
            stream = self.__streams.get(stream_name, None)

        if not stream:
            self.__logger.warning(f"Can't stop {stream_name}, stream not found in memory")
            return False, "Stream not found in memory"

        return stream.stop()

    def restart(self, stream_name: str):
        pass

    def reload(self, stream_name: str):
        pass

    # ==================================================================================================================
    # STATION TRANSMISSIONS
    # ==================================================================================================================

    def start_all_streams(self, station_id):
        """
        Start all streams for the station.

        :param station_id: Station database ID
        :return: Tuple (success, error_message)
        """
        streams = self.get_streams_by_station_id(station_id)

        if not streams:
            self.__logger.warning(f"No available streams for station {self.__station_name}")
            return False, "No available streams"

        errors = {}
        for stream in streams:
            _, error = self.start(stream.stream_name)

            if error:
                # Save start stream error
                errors[stream.stream_name] = error

        if errors:
            # Return start stream errors
            return False, errors

        return True, None

    def stop_all_streams(self):
        """
        Stop all streams from the station.

        :return: tuple
        """
        with self.__lock:
            streams = list(self.__streams.keys())

        errors = {}
        for stream_name in streams:
            _, error = self.stop(stream_name)

            if error:
                # Save stop stream error
                errors[stream_name] = error

        if errors:
            # Return stop stream errors
            return False, errors

        return True, None

    def restart_all_streams(self):
        pass

    def reload_all_streams(self):
        pass