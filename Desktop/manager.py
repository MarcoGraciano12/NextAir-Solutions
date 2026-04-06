from db import init_db
from controllers import *
from logging import Logger, getLogger


class Manager:

    def __init__(self, logger: Logger = None):

        if not init_db():
            raise RuntimeError("Failed to initialize database connection")

        self.__logger = logger or getLogger(self.__class__.__name__)

        self.__stream_inputs = StreamInputController()
        self.__device_inputs = DeviceInputController()
        self.__subjects = SubjectsController()

        self.__stations = StationController()
        self.__streams = StreamController()
        self.__broadcast = BroadcastController()
        self.__transmission = TransmissionController(subjects=self.__subjects)

        self.__sources = SourcesController()
        self.__playlist = PlaylistController()

    def init_subjects(self):
        """
        Initialize all device subjects from database records.

        :return: None
        """
        device_inputs = self.__device_inputs.get_all()

        if not device_inputs:
            self.__logger.warning(f"Failed to init device subjects")
            return

        # Create subject for each device input record
        for device in device_inputs:
            self.__subjects.add_device_subject(**device.to_dict())

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
    # DEVICE INPUT
    # ==================================================================================================================
    def create_device_input(self, **kwargs):
        """
        Creates a new audio input device.

        :param kwargs: Device fields (name, device_name, sample_rate, gpi, gpio)
        :return: Tuple (success: bool, result: DeviceInput or error message)
        """
        return self.__device_inputs.create(**kwargs)

    def retrieve_device_input(self, device_input_id: int):
        """
        Retrieves a single device input by ID.

        :param device_input_id: ID of the device to retrieve
        :return: Tuple (success: bool, result: DeviceInput or error message)
        """
        return self.__device_inputs.get(device_input_id=device_input_id)

    def update_device_input(self, **kwargs):
        """
        Updates an existing audio input device.

        :param kwargs: Fields to update including device_input_id
        :return: Tuple (success: bool, result: DeviceInput or error message)
        """
        return self.__device_inputs.update(**kwargs)

    def delete_device_input(self, name: str):
        """
        Deletes an audio input device by name.

        :param name: ID of the device to delete
        :return: Tuple (success: bool, message: str)
        """
        return self.__device_inputs.delete(name=name)

    def retrieve_all_device_input(self):
        """
        Retrieves all audio input devices.

        :return: List of DeviceInput objects or empty list
        """
        return self.__device_inputs.get_all()

    def retrieve_device_input_by_name(self, name: str):
        """
        Retrieves a device input by exact name match.

        :param name: Exact name of the device
        :return: Tuple (success: bool, result: DeviceInput or error message)
        """
        return self.__device_inputs.get_by_name(name=name)

    def retrieve_device_input_by_search(self, name: str):
        """
        Searches device inputs by partial name match.

        :param name: Search term for device name
        :return: List of matching DeviceInput objects or empty list
        """
        return self.__device_inputs.search_by_name(search_term=name)

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

    def delete_station(self, station_id: int):
        """
        Delete a station from the database by its ID.

        :param station_id: Unique identifier of the station to delete
        :return: Tuple (success: bool, message: str)
        """
        return self.__stations.delete(station_id)

    def create_station(self, *kwargs):
        """
        Create a new station in the database.

        :param kwargs: Station data (name, path, etc.)
        :return: Tuple (success: bool, station: Station) if success, or (False, error_message: str) if failed
        """
        return self.__stations.create(*kwargs)

    def search_stations(self, search_term: str):
        """
        Search stations by name with partial matching.

        :param search_term: Text to search in station names
        :return: Tuple (success: bool, stations: list or error_message: str)
        """
        return self.__stations.search_by_name(search_term)

    def create_many_stations(self, stations: list) -> tuple:
        """
        Creates multiple stations from a list of dictionaries.

        :param stations: List of dictionaries with station data
        :return: Tuple (success: bool, errors: list or None)
        """
        errors = []

        for station in stations:
            success, msg = self.__stations.create(
                station_name=station['station_name'],
                files_path=station['files_path']
            )

            if not success:
                errors.append(msg)

        if errors:
            return False, errors

        return True, None

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

    def create_many_streams(self, streams: list) -> tuple:
        """
        Creates multiple streams with their broadcasts from a list of dictionaries.

        :param streams: List of dictionaries with stream and broadcast data
        :return: Tuple (success: bool, errors: list or None)
        """
        errors = []

        for stream in streams:
            # Get station
            success, station = self.__stations.get_by_name(stream['station_name'])
            if not success:
                errors.append(station)
                continue

            # Create stream
            success, stream_model = self.__streams.create_stream(
                station_id=station.station_id,
                stream_name=stream['stream_name'],
                external_id=stream['external_id']
            )
            if not success:
                errors.append(stream_model)
                continue

            # Create broadcast
            success, msg = self.__broadcast.create(
                stream_id=stream_model.stream_id,
                name=stream['stream_name'],
                url=stream['url'],
                user=stream['user'],
                password=stream['password'],
                channels=stream['channels'],
                sample_rate=stream['sample_rate'],
                block_size=stream['block_size'],
                bitrate=stream['bitrate']
            )
            if not success:
                errors.append(msg)
                continue

        if errors:
            return False, errors

        return True, None

    def search_streams(self, search_term: str):
        """
        Search streams by name with partial matching.

        :param search_term: Texto to search in stream names
        :return: Tuple (success: bool, stations: list or error_message: str)
        """
        return self.__streams.search_by_name(search_term)

    # ==================================================================================================================
    # BROADCAST
    # ==================================================================================================================
    def create_broadcast(self, **kwargs):
        """
        Create broadcast configuration for a stream.

        :param kwargs: Broadcast attributes (stream_id, url, user, password, channels, sample_rate, block_size, bitrate)
        :return: Tuple (success: bool, broadcast or error_message)
        """
        return self.__broadcast.create(**kwargs)

    def delete_broadcast(self, broadcast_id: int):
        """
        Delete broadcast configuration from database.

        :param broadcast_id: ID of the broadcast to delete
        :return: Tuple (success: bool, message: str)
        """
        return self.__broadcast.delete(broadcast_id)

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

        return self.__transmission.start_transmission(**(stream.to_dict() | stream.broadcast.to_dict()))

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

    # ==================================================================================================================
    # PLAYLIST
    # ==================================================================================================================

    # ==================================================================================================================
    # SOURCES
    # ==================================================================================================================
    def get_stream_sources(self, stream_name: str, weekday: int):
        success, stream = self.__streams.get_by_name(stream_name)

        if not success:
            return False, stream

        return self.__sources.get_by_stream_and_weekday(stream_id=stream.stream_id, weekday=weekday)




