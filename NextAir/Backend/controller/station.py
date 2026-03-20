"""
Station management for streaming system.

Author: Marco Graciano
Date: March 20, 2026

Description: Station object that manages multiple audio streams.
"""

from .stream import Stream
from models import StreamModel
from logging import Logger, getLogger


class Station:
    """
    Radio station managing multiple audio streams.
    """

    def __init__(self, station_id: int, station_name: str, files_path: str, logger: Logger = None, **kwargs):
        """
        Initialize station instance.

        :param station_id: Station unique identifier
        :param station_name: Station name
        :param files_path: Path to audio files directory
        :param logger: Logger instance
        :return: None
        """
        self.__streams = {}
        self.__station_id = station_id
        self.__files_path = files_path
        self.__station_name = station_name
        self.__logger = logger or getLogger(self.__station_name)

    @property
    def station_id(self) -> int:
        """
        Get station ID.
        """
        return self.__station_id

    @property
    def station_name(self) -> str:
        """
        Get station name.
        """
        return self.__station_name

    @property
    def files_path(self) -> str:
        """
        Get files path.
        """
        return self.__files_path

    def __str__(self) -> str:
        """
        String representation of station.

        :return: Formatted string with station attributes
        """
        return f"station_name: {self.__station_name}, files_path: {self.__files_path}"

    def start(self, stream_name: str) -> dict:
        """
        Start stream transmission.

        :param stream_name: Stream name
        :return: Dict with status and message
        """
        # Check cache
        stream = self.__streams.get(stream_name)

        if stream:
            return stream.start()

        # Load from DB
        stream_model = StreamModel.find_by_name(stream_name)

        if not stream_model:
            self.__logger.warning(f"Stream '{stream_name}' not found")
            return {'status': False, 'message': f"Stream '{stream_name}' not found"}

        # Create and start
        stream = Stream(**stream_model.to_dict())
        self.__logger.info(f"Stream loaded: {stream}")
        result = stream.start()

        if not result['status']:
            self.__logger.error(f"Failed to start stream '{stream_name}': {result['message']}")
            return result

        # Cache only if started successfully
        self.__streams[stream_name] = stream
        return result

    def stop(self, stream_name: str) -> dict:
        """
        Stop stream transmission.

        :param stream_name: Stream name
        :return: Dict with status and message
        """
        stream = self.__streams.get(stream_name)

        if not stream:
            self.__logger.warning(f"Stream '{stream_name}' not found in memory")
            return {'status': False, 'message': f"Stream '{stream_name}' not active"}

        result = stream.stop()
        return result

    def restart(self, stream_name: str) -> dict:
        """
        Restart stream transmission.

        :param stream_name: Stream name
        :return: Dict with status and message
        """
        self.stop(stream_name)
        return self.start(stream_name)

    def reload(self, stream_name: str) -> dict:
        """
        Reload stream configuration.

        :param stream_name: Stream name
        :return: Dict with status and message
        """
        stream = self.__streams.get(stream_name)

        if not stream:
            self.__logger.warning(f"Stream '{stream_name}' not found in memory")
            return {'status': False, 'message': f"Stream '{stream_name}' not active"}

        result = stream.reload()
        return result
