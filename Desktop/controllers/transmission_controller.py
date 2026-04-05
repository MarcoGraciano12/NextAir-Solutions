"""
Stream management for audio broadcasting.

Author: Marco Graciano
Date: March 20, 2026

Description: Stream object managing encoding, broadcasting and observer pattern.
"""

from datetime import datetime
from logging import Logger, getLogger
from threading import Thread, Lock, Event
from scripts import get_weekday_sources, update_sources, update_schedule_block, get_schedule_block


# class Transmission:
#     """
#     Audio stream managing encoding and broadcasting operations.
#     """
#
#     def __init__(self, stream_id: int, stream_name: str, external_id: int, logger: Logger = None, **kwargs):
#         """
#         Initialize stream instance.
#
#         :param stream_id: Stream unique identifier
#         :param stream_name: Stream name
#         :param external_id: External system identifier
#         :param logger: Logger instance
#         :return: None
#         """
#         self.__broadcast = None
#         self.__encoder = None
#         self.__observer = None
#
#         self.__stream_thread = None
#         self.__stop_stream = Event()
#         self.__stream_lock = Lock()
#
#         self.__stream_id = stream_id
#         self.__stream_name = stream_name
#         self.__external_id = external_id
#         self.__logger = logger or getLogger(self.__stream_name)
#
#     @property
#     def stream_id(self) -> int:
#         """
#         Get stream ID.
#         """
#         return self.__stream_id
#
#     @property
#     def stream_name(self) -> str:
#         """
#         Get stream name.
#         """
#         return self.__stream_name
#
#     @stream_name.setter
#     def stream_name(self, value: str):
#         """
#         Set stream name.
#
#         :param value: New stream name
#         """
#         self.__stream_name = value
#
#     @property
#     def external_id(self) -> int:
#         """
#         Get external ID.
#         """
#         return self.__external_id
#
#     @external_id.setter
#     def external_id(self, value: int):
#         """
#         Set external ID.
#
#         :param value: New external ID
#         """
#         self.__external_id = value
#
#     def __str__(self) -> str:
#         """
#         String representation of stream.
#
#         :return: Formatted string with stream attributes
#         """
#         return f"stream_name: {self.__stream_name}, external_id: {self.__external_id}, observer: {self.__observer}"
#
#     # ==================================================================================================================
#     # TRANSMISSION
#     # ==================================================================================================================
#
#     def __commercial_transition(self):
#         pass
#
#     def __manual_transition(self):
#         pass
#
#     def __automatic_transition(self):
#         pass
#
#     def __transition_core(self):
#         pass
#
#     def __init_transmission(self, date: datetime):
#         """
#         Initialize transmission by loading or updating sources and playlist.
#
#         :param date: Datetime to initialize
#         :return: Tuple of (sources, playlist) or None if failed
#         """
#         # Try to get sources from database
#         sources = get_weekday_sources(self.__stream_id, date.weekday())
#
#         if not sources:
#             # Sources not found, fetch and update from external source
#             sources = update_sources(self.__external_id, self.__stream_id, date.weekday(), date)
#
#             if not sources:
#                 # Failed to update sources
#                 return None
#
#         # Try to get playlist block from database
#         playlist = get_schedule_block(self.__stream_id, date, date.hour)
#
#         if not playlist:
#             # Playlist not found, fetch and update from external source
#             playlist = update_schedule_block(self.__external_id, self.__stream_id, date, date.hour)
#
#             if not playlist:
#                 # Failed to update playlist
#                 return None
#
#         # Return both sources and playlist
#         return sources, playlist
#
#     @property
#     def is_running(self):
#         """
#         Check if stream is currently running.
#
#         :return: True if running, False otherwise
#         """
#         return not self.__stop_stream.is_set()
#
#     def __loop(self):
#         """
#         Main streaming loop.
#
#         :return: True if completed successfully, False on error
#         """
#         try:
#             now = datetime.now()
#
#             # Initialize transmission data
#             result = self.__init_transmission(now)
#
#             if not result:
#                 # Failed to initialize transmission
#                 self.__logger.error("Failed to initialize transmission")
#                 self.__stop_stream.set()
#                 return  # O lo que corresponda
#
#             # Unpack sources and playlist
#             sources, playlist = result
#
#             while not self.__stop_stream.is_set():
#                 for source in sources:
#                     print(source.to_dict())
#
#                 for item in playlist:
#                     print(item.to_dict())
#
#                 self.__stop_stream.wait(10)
#
#         except Exception as e:
#             self.__logger.error(f"Stream loop error: {e}")
#             return False
#
#         finally:
#             # Cleanup resources here (close connections, files, etc.)
#             self.__logger.info("Stream loop stopped")
#
#         return True
#
#     def start(self):
#         """
#         Start audio streaming to broadcast server.
#
#         :return: tuple
#         """
#         with self.__stream_lock:
#             # Check if stream is already active
#             if self.__stream_thread is not None and self.__stream_thread.is_alive():
#                 self.__logger.warning("Stream already running")
#                 return False, "Stream already running"
#
#             # Reset stop signal and create new thread
#             self.__stop_stream.clear()
#             self.__stream_thread = Thread(target=self.__loop, daemon=False)
#             self.__stream_thread.start()
#
#             self.__logger.info("Stream started successfully")
#             return True, None
#
#     def stop(self):
#         """
#         Stop audio streaming gracefully.
#
#         :return: Tuple
#         """
#         with self.__stream_lock:
#             # Check if stream is running
#             if self.__stream_thread is None or not self.__stream_thread.is_alive():
#                 self.__logger.warning("Stream not running")
#                 return False, "Stream not running"
#
#             # Signal thread to stop
#             self.__stop_stream.set()
#
#         # Wait for thread to finish (outside lock to avoid deadlock)
#         self.__stream_thread.join()
#         self.__logger.info("Stream stopped Successfully")
#         return True, None
#
#     def restart(self):
#         pass
#
#     def reload(self):
#         pass

class Transmission:
    """
    Audio stream managing encoding and broadcasting operations.
    """

    def __init__(self, stream_id: int, station_id: int, stream_name: str, external_id: int, url: str, user: str,
            password: str, channels: int, sample_rate: int, block_size: int, bitrate: str, logger: Logger = None, **kwargs):
        """
        Initialize stream instance.

        :param stream_id: Stream unique identifier
        :param station_id: Station identifier
        :param stream_name: Stream name
        :param external_id: External system identifier
        :param url: Broadcast URL
        :param user: Broadcast user
        :param password: Broadcast password
        :param channels: Audio channels
        :param sample_rate: Audio sample rate
        :param block_size: Audio block size
        :param bitrate: Audio bitrate
        :param logger: Logger instance
        :return: None
        """
        # Stream identifiers and configuration parameters
        self.__stream_id = stream_id
        self.__station_id = station_id
        self.__stream_name = stream_name
        self.__external_id = external_id

        # Broadcast server connection settings
        self.__url = url
        self.__user = user
        self.__password = password

        # Audio processing parameters
        self.__bitrate = bitrate
        self.__channels = channels
        self.__block_size = block_size
        self.__sample_rate = sample_rate

        # Logging instance for stream operations
        self.__logger = logger or getLogger(stream_name)

        # Audio pipeline components (initialized on start)
        self.__encoder = None
        self.__observer = None
        self.__broadcast = None

        # Thread management and synchronization primitives
        self.__stream_thread = None
        self.__stream_lock = Lock()
        self.__stop_stream = Event()

    @property
    def stream_id(self) -> int:
        """
        Stream unique identifier.
        """
        return self.__stream_id

    @property
    def station_id(self) -> int:
        """
        Station identifier.
        """
        return self.__station_id

    @property
    def stream_name(self) -> str:
        """
        Stream name.
        """
        return self.__stream_name

    @property
    def external_id(self) -> int:
        """
        External system identifier.
        """
        return self.__external_id

    @property
    def url(self) -> str:
        """
        Broadcast URL.
        """
        return self.__url

    @property
    def user(self) -> str:
        """
        Broadcast user.
        """
        return self.__user

    @property
    def password(self) -> str:
        """
        Broadcast password.
        """
        return self.__password

    @property
    def channels(self) -> int:
        """
        Audio channels.
        """
        return self.__channels

    @property
    def sample_rate(self) -> int:
        """
        Audio sample rate.
        """
        return self.__sample_rate

    @property
    def block_size(self) -> int:
        """
        Audio block size.
        """
        return self.__block_size

    @property
    def bitrate(self) -> str:
        """
        Audio bitrate.
        """
        return self.__bitrate

    def __str__(self) -> str:
        """
        String representation of the transmission.
        """
        return f"{self.stream_name} | {self.sample_rate}Hz | {self.block_size} | {self.channels}ch | {self.bitrate}"

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
            # now = datetime.now()
            #
            # # Initialize transmission data
            # result = self.__init_transmission(now)
            #
            # if not result:
            #     # Failed to initialize transmission
            #     self.__logger.error("Failed to initialize transmission")
            #     self.__stop_stream.set()
            #     return  # O lo que corresponda
            #
            # # Unpack sources and playlist
            # sources, playlist = result

            while not self.__stop_stream.is_set():
                # for source in sources:
                #     print(source.to_dict())
                #
                # for item in playlist:
                #     print(item.to_dict())
                self.__logger.info(f"Transmission {self.__stream_name} running")
                self.__stop_stream.wait(10)

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


class TransmissionController:

    def __init__(self, logger: Logger = None):
        """
        Initialize station controller.

        :param logger: Logger instance
        :return: None
        """
        self.__transmissions = {}
        self.__lock = Lock()
        self.__logger = logger or getLogger(self.__class__.__name__)

    def start_transmission(self, stream_name: str, **kwargs):
        """
        Start a stream transmission.

        :param stream_name: Stream identifier
        :param kwargs: Transmission parameters
        :return: Tuple (success: bool, result or error message)
        """
        with self.__lock:
            transmission = self.__transmissions.get(stream_name, None)

        if not transmission:
            self.__logger.info(f"{stream_name} transmission, not found, build new transmission")
            transmission = Transmission(stream_name=stream_name, **kwargs)

        with self.__lock:
            if stream_name not in self.__transmissions:
                self.__transmissions[stream_name] = transmission
                self.__logger.info(f"{stream_name} added to transmissions")
            else:
                transmission = self.__transmissions[stream_name]
                self.__logger.info(f"{stream_name} already in transmissions (added by another thread)")

        return transmission.start()

    def stop_transmission(self, stream_name: str):
        """
        Stop a stream transmission.

        :param stream_name: Stream identifier
        :return: Tuple (success: bool, result or error message)
        """
        with self.__lock:
            transmission = self.__transmissions.get(stream_name, None)

        if not transmission:
            self.__logger.warning(f"Can't stop {stream_name}, transmission not found in current transmissions")
            return False, f"{stream_name} not found in transmissions"

        return transmission.stop()
