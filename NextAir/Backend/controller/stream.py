"""
Stream management for audio broadcasting.

Author: Marco Graciano
Date: March 20, 2026

Description: Stream object managing encoding, broadcasting and observer pattern.
"""

from encoders import OGG
from broadcasts import Icecast
from observers import StreamObserver
from logging import Logger, getLogger
from threading import Thread, Lock, Event


class Stream:
    """
    Audio stream managing encoding and broadcasting operations.
    """

    def __init__(self, stream_name: str, external_id: int, logger: Logger = None, **kwargs):
        """
        Initialize stream instance.

        :param stream_name: Stream name
        :param external_id: External system identifier
        :param logger: Logger instance
        :return: None
        """
        self.__broadcast = None
        self.__encoder = None
        self.__observer = None

        self.__stream_thread = None
        self.__stream_stop = Event()
        self.__stream_lock = Lock()

        self.__stream_name = stream_name
        self.__external_id = external_id
        self.__logger = logger or getLogger(self.__stream_name)

    @property
    def stream_name(self) -> str:
        """
        Get stream name.
        """
        return self.__stream_name

    @stream_name.setter
    def stream_name(self, value: str):
        """
        Set stream name.

        :param value: New stream name
        """
        self.__stream_name = value

    @property
    def external_id(self) -> int:
        """
        Get external ID.
        """
        return self.__external_id

    @external_id.setter
    def external_id(self, value: int):
        """
        Set external ID.

        :param value: New external ID
        """
        self.__external_id = value

    def __str__(self) -> str:
        """
        String representation of stream.

        :return: Formatted string with stream attributes
        """
        return f"stream_name: {self.__stream_name}, external_id: {self.__external_id}, observer: {self.__observer}"





    #
    # def start(self) -> dict:
    #     """
    #     Start stream transmission.
    #
    #     :return: Dict with status and message
    #     """
    #     self.__logger.info("Stream started successfully")
    #     return {'status': True}
    #
    # def stop(self) -> dict:
    #     """
    #     Stop stream transmission.
    #
    #     :return: Dict with status and message
    #     """
    #     self.__logger.info("Stream stopped successfully")
    #     return {'status': True}
    #
    # def restart(self) -> dict:
    #     """
    #     Restart stream transmission.
    #
    #     :return: Dict with status and message
    #     """
    #     self.__logger.info("Stream restarted successfully")
    #     return {'status': True}
    #
    # def reload(self) -> dict:
    #     """
    #     Reload stream configuration.
    #
    #     :return: Dict with status and message
    #     """
    #     self.__logger.info("Stream reloaded successfully")
    #     return {'status': True}
