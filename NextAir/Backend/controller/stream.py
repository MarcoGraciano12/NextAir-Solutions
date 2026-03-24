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
        self.__stop_stream = Event()
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

    # ==================================================================================================================
    # SINGLE TRANSMISSION
    # ==================================================================================================================

    @property
    def is_running(self):
        """
        Check if stream is currently running.

        :return: True if running, False otherwise
        """
        return not self.__stop_stream.is_set()

    def __loop(self):
        """
        Main streaming loop.

        :return: True if completed successfully, False on error
        """
        try:
            self.__logger.info("Stream loop started")

            while not self.__stop_stream.is_set():
                self.__logger.debug("Streaming audio chunk")

                # Wait 5 seconds or until stop signal
                self.__stop_stream.wait(5)

        except Exception as e:
            self.__logger.error(f"Stream loop error: {e}")
            return False

        finally:
            # Cleanup resources here (close connections, files, etc.)
            self.__logger.info("Stream loop stopped")

        return True

    def start(self):
        """
        Start audio streaming to broadcast server.

        :return: tuple
        """
        with self.__stream_lock:
            # Check if stream is already active
            if self.__stream_thread is not None and self.__stream_thread.is_alive():
                self.__logger.warning("Stream already running")
                return False, "Stream already running"

            # Reset stop signal and create new thread
            self.__stop_stream.clear()
            self.__stream_thread = Thread(target=self.__loop, daemon=False)
            self.__stream_thread.start()

            self.__logger.info("Stream started successfully")
            return True, None

    def stop(self):
        """
        Stop audio streaming gracefully.

        :return: Tuple
        """
        with self.__stream_lock:
            # Check if stream is running
            if self.__stream_thread is None or not self.__stream_thread.is_alive():
                self.__logger.warning("Stream not running")
                return False, "Stream not running"

            # Signal thread to stop
            self.__stop_stream.set()

        # Wait for thread to finish (outside lock to avoid deadlock)
        self.__stream_thread.join()
        self.__logger.info("Stream stopped Successfully")
        return True, None

    def restart(self):
        pass

    def reload(self):
        pass

