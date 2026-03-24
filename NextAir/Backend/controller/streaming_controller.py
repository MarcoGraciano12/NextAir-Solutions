"""
Station controller for broadcasting system.

Author: Marco Graciano
Date: March 22, 2026

Description: Manages CRUD operations for radio stations with thread-safe access.
"""

from threading import Lock
from .station import Station
from models import StationModel
from logging import Logger, getLogger


class StreamingController:
    """
    Controller for managing radio stations.
    Handles CRUD operations with thread-safe access to station instances.
    """

    def __init__(self, stream_input_controller, logger: Logger = None):
        """
        Initialize station controller.

        :param logger: Logger instance
        :return: None
        """
        self.__stations = {}  # station_name -> Station
        self.__lock = Lock()
        self.__stream_input_controller = stream_input_controller
        self.__logger = logger or getLogger(self.__class__.__name__)

    def initialize(self):
        """
        Load existing stations from database into memory on startup.

        :return: None
        """
        try:
            self.__logger.info("Initializing stations from database")

            # Retrieve all station records
            models = StationModel.get_all()

            # Create in-memory objects for each database record
            for model in models:
                station = Station(model.station_name, model.files_path, self.__stream_input_controller)

                station.initialize(model.station_id)  # Initialize streams

                # Register station
                self.__stations[model.station_name] = station

            self.__logger.info(f"Loaded {len(models)} stations from database")

        except Exception as error:
            self.__logger.error(f"Failed to initialize stations: {error}")

    # ==================================================================================================================
    # STATIONS
    # ==================================================================================================================

    def create_station(self, station_name: str, files_path: str):
        """
        Create and register a new radio station.

        :param station_name: Station name
        :param files_path: Path to audio files directory
        :return: Tuple (StationModel, message) - model is None on error
        """
        try:
            # Validate name uniqueness
            if StationModel.find_by_name(station_name):
                self.__logger.warning(f"Station name already exists: {station_name}")
                return None, "A station with that name already exists"

            with self.__lock:
                # Check if station already exists in memory
                if station_name in self.__stations:
                    self.__logger.warning(f"Station already in memory: {station_name}")
                    return None, "Station already exists"

                # Save to database
                station_model = StationModel(station_name=station_name, files_path=files_path)
                station_model.save_to_db()

                # Create station object
                self.__stations[station_name] = Station(station_name, files_path, self.__stream_input_controller)

            self.__logger.info(f"Station created: {station_name}")
            return station_model, None

        except Exception as error:
            self.__logger.error(f"Error creating station: {error}")
            return None, f"Failed to create station: {str(error)}"

    def retrieve_station(self, station_name: str):
        """
        Get a station from database by name.

        :param station_name: Station name
        :return: Tuple (StationModel, message) - model is None on error
        """
        try:
            station_model = StationModel.find_by_name(station_name)

            if not station_model:
                self.__logger.warning(f"Station not found with name: {station_name}")
                return None, "Station not found"

            return station_model, None

        except Exception as error:
            self.__logger.error(f"Error retrieving station: {error}")
            return None, f"Failed to retrieve station: {str(error)}"

    def retrieve_all_stations(self):
        """
        Get all stations from database.

        :return: Tuple (list of StationModel, message) - list is None on error
        """
        try:
            stations = StationModel.get_all()
            return stations, None

        except Exception as error:
            self.__logger.error(f"Error retrieving stations: {error}")
            return None, f"Failed to retrieve stations: {str(error)}"

    def delete_station(self, station_name: str):
        """
        Delete a station and stop all its streams.

        :param station_name: Station name
        :return: Tuple (StationModel, message) - model is None on error
        """
        try:
            # Get station from database
            station_model = StationModel.find_by_name(station_name)

            if not station_model:
                self.__logger.warning(f"Station not found with name: {station_name}")
                return None, "Station not found"

            # Get station object from memory
            with self.__lock:
                station = self.__stations.get(station_name)

            # Stop all streams if exists in memory
            if station:
                if not station.stop_all_streams():
                    self.__logger.error(f"Failed to stop streams for station: {station_name}")
                    # return None, "Failed to stop station streams"

                # Remove from memory after successful stop
                with self.__lock:
                    self.__stations.pop(station_name, None)

            # Delete from database
            station_model.delete_from_db()

            self.__logger.info(f"Station deleted: {station_name}")
            return station_model, None

        except Exception as error:
            self.__logger.error(f"Error deleting station: {error}")
            return None, f"Failed to delete station: {str(error)}"

    # ==================================================================================================================
    # STREAMS
    # ==================================================================================================================

    def create_stream(self, station_name: str, **kwargs):
        """
        Create a new stream for a station.

        :param station_name: Station name
        :param kwargs: Stream configuration parameters
        :return: Tuple (StreamModel, message) - model is None on error
        """
        # Get station model from DB to get station_id
        station_model = StationModel.find_by_name(station_name)

        if not station_model:
            self.__logger.warning(f"Station not found in DB: {station_name}")
            return None, "Station not found"

        # Get station from memory
        with self.__lock:
            station = self.__stations.get(station_name)

        if not station:
            self.__logger.warning(f"Station not in memory: {station_name}")
            return None, "Station not found"

        # Delegate with station_id
        return station.create_stream(station_model.station_id, **kwargs)

    @staticmethod
    def retrieve_stream(stream_name: str):
        """
        Get a stream by name.

        :param stream_name: Stream name
        :return: Tuple (StreamModel, message) - model is None on error
        """
        try:
            stream_model = Station.find_stream_by_name(stream_name)

            if not stream_model:
                return None, "Stream not found"

            return stream_model, None

        except Exception as error:
            return None, f"Failed to retrieve stream: {str(error)}"

    @staticmethod
    def retrieve_all_streams():
        """
        Get all streams from all stations.

        :return: Tuple (list of StreamModel, message) - list is None on error
        """
        try:
            streams = Station.get_all_streams()
            return streams, None

        except Exception as error:
            return None, f"Failed to retrieve streams: {str(error)}"

    @staticmethod
    def retrieve_streams_for_station(station_name: str):
        """
        Get all streams for a specific station.

        :param station_name: Station name
        :return: Tuple (list of StreamModel, message) - list is None on error
        """
        try:
            # Get station model to get station_id
            station_model = StationModel.find_by_name(station_name)

            if not station_model:
                return None, "Station not found"

            return Station.get_streams_by_station_id(station_model.station_id), None

        except Exception as error:
            return None, f"Failed to retrieve streams: {str(error)}"

    def delete_stream(self, stream_name: str):
        """
        Delete a stream by name.

        :param stream_name: Stream name
        :return: Tuple (StreamModel, message) - model is None on error
        """
        try:
            # Get stream from database
            stream_model = Station.find_stream_by_name(stream_name)

            if not stream_model:
                self.__logger.warning(f"Stream not found in DB: {stream_name}")
                return None, "Stream not found"

            # Get station from database
            station_model = StationModel.find_by_id(stream_model.station_id)

            if not station_model:
                self.__logger.warning(f"Station not found in DB for stream: {stream_name}")
                return None, "Station not found"

            # Get station from memory
            with self.__lock:
                station = self.__stations.get(station_model.station_name)

            if not station:
                self.__logger.warning(f"Station not in memory: {station_model.station_name}")
                return Station.delete_stream_by_name(stream_name)

            # Delete stream from memory (stops and removes)
            return station.delete_stream(stream_name)

        except Exception as error:
            self.__logger.error(f"Error deleting stream: {error}")
            return None, f"Failed to delete stream: {str(error)}"

    # ==================================================================================================================
    # SINGLE TRANSMISSION
    # ==================================================================================================================

    def start_transmission(self, station_name: str, stream_name: str):
        pass

    def stop_transmission(self, station_name: str, stream_name: str):
        pass

    def restart_transmission(self, station_name: str, stream_name: str):
        pass

    def reload_transmission(self, station_name: str, stream_name: str):
        pass

    # ==================================================================================================================
    # STATION TRANSMISSIONS
    # ==================================================================================================================

    def start_station_transmissions(self, station_name: str):
        pass

    def stop_station_transmissions(self, station_name: str):
        pass

    def restart_station_transmissions(self, station_name: str):
        pass

    def reload_station_transmissions(self, station_name: str):
        pass

    # ==================================================================================================================
    # ALL TRANSMISSIONS
    # ==================================================================================================================

    def start_all_transmissions(self):
        pass

    def stop_all_transmissions(self):
        pass

    def restart_all_transmissions(self):
        pass

    def reload_all_transmissions(self):
        pass
