from db import init_db
from controllers import *
from logging import Logger, getLogger


class Manager:

    def __init__(self, logger: Logger = None):

        if not init_db():
            raise "Failed to initialize database connection"

        self.__logger = logger or getLogger(self.__class__.__name__)

        self.__stream_inputs = StreamInputController()
        self.__subjects = SubjectsController()

        self.__stations = StationController()
        self.__streams = StreamController()
        self.__broadcast = BroadcastController()
        self.__transmission = TransmissionController()

    def init_subjects(self):
        success, items = self.__stream_inputs.get_all()

        if not success:
            return False, items

        for item in items:
            self.__subjects.add_stream_subject(**item.to_dict())

    # ==================================================================================================================
    # STREAM INPUT
    # ==================================================================================================================
    def create_stream_input(self, **kwargs):
        """
        Creates a stream input and registers its subject.

        :param kwargs: Stream configuration parameters (must include required fields)
        :return: Tuple (success: bool, stream_subject or error_message)
        """
        success, content = self.__stream_inputs.create(**kwargs)

        if not success:
            return False, content

        return self.__subjects.add_stream_subject(**kwargs)

    def delete_stream_input(self, input_id: int):
        """
        Deletes a stream input and removes its subject.

        :param input_id: Database ID of the stream input
        :return: Tuple (success: bool, confirmation or error_message)
        """
        success, content = self.__stream_inputs.delete(stream_input_id=input_id)

        if not success:
            return False, content

        return self.__subjects.remove_stream_subject(name=content.name)

    def get_stream_subjects(self):
        return self.__subjects.stream_subjects

    def get_stream_inputs(self):
        return self.__stream_inputs.get_all()

    # ==================================================================================================================
    # STATIONS
    # ==================================================================================================================
    def get_station(self, station_name: str):
        """
        Retrieves a station by name.

        :param station_name: Name of the station to retrieve
        :return: Tuple (success: bool, station or error_message)
        """
        return self.__stations.get_by_name(station_name=station_name)

    def get_all_stations(self):
        """
        Retrieves all stations.

        :return: Tuple (success: bool, station_list or error_message)
        """
        return self.__stations.get_all()

    # ==================================================================================================================
    # STREAMS
    # ==================================================================================================================
    def create_stream(self, **kwargs):
        """
        Creates a new stream record.

        :param kwargs: Stream attributes (stream_name, etc.)
        :return: Tuple (success: bool, stream or error_message)
        """
        return self.__streams.create(**kwargs)

    def delete_stream(self, stream_name: str):
        """
        Deletes a stream by name.

        :param stream_name: Name of the stream to delete
        :return: Tuple (success: bool, confirmation or error_message)
        """
        return self.__streams.delete(stream_name=stream_name)

    def get_stream(self, stream_name: str):
        """
        Retrieves a stream by name.

        :param stream_name: Name of the stream to retrieve
        :return: Tuple (success: bool, stream or error_message)
        """
        return self.__streams.get_by_name(stream_name=stream_name)

    def get_all_streams(self):
        """
        Retrieves all streams.

        :return: Tuple (success: bool, stream_list or error_message)
        """
        return self.__streams.get_all()

    def get_streams_by_station(self, station_id: int):
        return self.__streams.get_by_station(station_id=station_id)
    # ==================================================================================================================
    # BROADCAST
    # ==================================================================================================================

    # ==================================================================================================================
    # SINGLE TRANSMISSIONS
    # ==================================================================================================================
    def start_transmission(self, stream_name: str):
        """
        Starts transmission for a stream.

        :param stream_name: Name of the stream to start
        :return: Tuple (success: bool, transmission or error_message)
        """
        success, stream = self.__streams.get_by_name(stream_name)

        if not success:
            return False, stream

        return self.__transmission.start_transmission(**stream.to_dict())

    def stop_transmission(self, stream_name: str):
        """
        Stops transmission for a stream.

        :param stream_name: Name of the stream to stop
        :return: Tuple (success: bool, confirmation or error_message)
        """
        return self.__transmission.stop_transmission(stream_name=stream_name)

    # ==================================================================================================================
    # STATION TRANSMISSIONS
    # ==================================================================================================================
    def start_station_transmission(self, station_name: str):
        """
        Starts transmission for all streams of a station.

        :param station_name: Name of the station
        :return: Tuple (success: bool, confirmation or error_dict)
        """
        success, station = self.__stations.get_by_name(station_name)

        if not success:
            return False, station

        success, streams = self.__streams.get_by_station(station.station_id)

        if not success:
            return False, streams

        errors = {}
        for stream in streams:
            _, error = self.start_transmission(stream.stream_name)

            if error:
                errors[stream.stream_name] = error

        if errors:
            return False, errors

        return True, None

    def stop_station_transmission(self, station_name: str):
        """
        Stops transmission for all streams of a station.

        :param station_name: Name of the station
        :return: Tuple (success: bool, confirmation or error_dict)
        """
        success, station = self.__stations.get_by_name(station_name)

        if not success:
            return False, station

        success, streams = self.__streams.get_by_station(station.station_id)

        if not success:
            return False, streams

        errors = {}
        for stream in streams:
            _, error = self.stop_transmission(stream.stream_name)

            if error:
                errors[stream.stream_name] = error

        if errors:
            return False, errors

        return True, None

    # ==================================================================================================================
    # ALL TRANSMISSIONS
    # ==================================================================================================================






