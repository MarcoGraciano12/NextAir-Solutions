"""
Controller for streaming system management.

Author: Marco Graciano
Date: March 20, 2026

Description: Main controller for managing radio stations and audio streaming operations.
"""

from logging import Logger, getLogger
from .stream_input_controller import StreamInputController
from .streaming_controller import StreamingController


class Controller:

    def __init__(self, logger: Logger = None):

        self.__stream_input_controller = StreamInputController()
        self.__transmission_controller = StreamingController(self.__stream_input_controller)

        self.__logger = logger or getLogger(self.__class__.__name__)

    def initialize(self):
        """
        Initialize all subsystems.

        :return: None
        """
        self.__stream_input_controller.initialize()
        self.__transmission_controller.initialize()

    # ==================================================================================================================
    # STREAM INPUTS
    # ==================================================================================================================

    def create_stream_input(self, **kwargs):
        """
        Add a new stream input.

        :param kwargs: Stream input configuration parameters
        :return: StreamInputModel if created, None if error
        """
        return self.__stream_input_controller.create_input(**kwargs)

    def retrieve_stream_input(self, **kwargs):
        """
        Get a stream input by ID.

        :param kwargs: Query parameters (stream_input_id)
        :return: StreamInputModel if found, None otherwise
        """
        return self.__stream_input_controller.retrieve_input(**kwargs)

    def retrieve_all_stream_inputs(self):
        """
        Get all stream inputs.

        :return: Tuple (list of StreamInputModel, message) - list is None on error
        """
        return self.__stream_input_controller.retrieve_all_inputs()

    def delete_stream_input(self, **kwargs):
        """
        Delete a stream input.

        :param kwargs: Query parameters (stream_input_id)
        :return: Tuple (StreamInputModel, message) - model is None on error
        """
        return self.__stream_input_controller.delete_input(**kwargs)

    def get_stream_inputs_status(self):
        """
        Get status of all stream inputs.

        :return: Tuple (list of status dicts, message) - list is None on error
        """
        return self.__stream_input_controller.get_inputs_status()

    # ==================================================================================================================
    # STATIONS
    # ==================================================================================================================

    def create_station(self, **kwargs):
        """
        Add a new station.

        :param kwargs: Station configuration parameters
        :return: Tuple (StationModel, message) - model is None on error
        """
        return self.__transmission_controller.create_station(**kwargs)

    def retrieve_station(self, **kwargs):
        """
        Get a station by name.

        :param kwargs: Query parameters (station_name)
        :return: Tuple (StationModel, message) - model is None on error
        """
        return self.__transmission_controller.retrieve_station(**kwargs)

    def retrieve_all_stations(self):
        """
        Get all stations.

        :return: Tuple (list of StationModel, message) - list is None on error
        """
        return self.__transmission_controller.retrieve_all_stations()

    def delete_station(self, **kwargs):
        """
        Delete a station.

        :param kwargs: Query parameters (station_name)
        :return: Tuple (StationModel, message) - model is None on error
        """
        return self.__transmission_controller.delete_station(**kwargs)

    # ==================================================================================================================
    # STREAMS
    # ==================================================================================================================

    def create_stream(self, **kwargs):
        """
        Create a new stream.

        :param kwargs: Stream configuration parameters (station_name, stream_name, external_id, etc.)
        :return: Tuple (StreamModel, message) - model is None on error
        """
        return self.__transmission_controller.create_stream(**kwargs)

    def get_stream(self, **kwargs):
        """
        Get a stream.

        :param kwargs: Query parameters (station_name, stream_name)
        :return: Tuple (StreamModel, message) - model is None on error
        """
        return self.__transmission_controller.retrieve_stream(**kwargs)

    def get_all_streams(self):
        """
        Get all streams.

        :return: Tuple (list of StreamModel, message) - list is None on error
        """
        return self.__transmission_controller.retrieve_all_streams()

    def get_streams_for_station(self, **kwargs):
        """
        Get all streams for a station.

        :param kwargs: Query parameters (station_name)
        :return: Tuple (list of StreamModel, message) - list is None on error
        """
        return self.__transmission_controller.retrieve_streams_for_station(**kwargs)

    def delete_stream(self, **kwargs):
        """
        Delete a stream.

        :param kwargs: Query parameters (station_name, stream_name)
        :return: Tuple (StreamModel, message) - model is None on error
        """
        return self.__transmission_controller.delete_stream(**kwargs)

    # ==================================================================================================================
    # SINGLE TRANSMISSION
    # ==================================================================================================================

    def start_transmission(self, **kwargs):
        pass

    def stop_transmission(self, **kwargs):
        pass

    def restart_transmission(self, **kwargs):
        pass

    def reload_transmission(self, **kwargs):
        pass

    # ==================================================================================================================
    # STATION TRANSMISSIONS
    # ==================================================================================================================

    def start_station_transmissions(self, **kwargs):
        pass

    def stop_station_transmissions(self, **kwargs):
        pass

    def restart_station_transmissions(self, **kwargs):
        pass

    def reload_station_transmissions(self, **kwargs):
        pass

    # ==================================================================================================================
    # ALL TRANSMISSIONS
    # ==================================================================================================================

    def start_all_transmissions(self, **kwargs):
        pass

    def stop_all_transmissions(self, **kwargs):
        pass

    def restart_all_transmissions(self, **kwargs):
        pass

    def reload_all_transmissions(self, **kwargs):
        pass