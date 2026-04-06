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


class Schedule:

    def __init__(self, stream_id: int, external_id: int, logger: Logger = None):
        """
        :param external_id: External system identifier
        """
        self.stream_id = stream_id
        self.external_id = external_id

        self.__sources = []
        self.__playlist = []

        # Thread management and synchronization primitives
        self.__thread = None
        self.__lock = Lock()
        self.__stop_thread = Event()
        self.__logger = logger or getLogger(self.__class__.__name__)

    def get_source(self):
        """
        Get a copy of the current sources list.

        :return: Copy of sources list or None if not initialized
        """
        with self.__lock:
            return self.__sources.copy() if self.__sources else None

    def get_playlist(self):
        """
        Get a copy of the current playlist.

        :return: Copy of playlist or None if not initialized
        """
        with self.__lock:
            return self.__playlist.copy() if self.__playlist else None

    def __init_schedule(self):
        """
        Initialize schedule configuration from database or external source.

        Attempts to load sources and playlist from database first. If not found,
        fetches and updates from external source.

        :return: Tuple (sources, playlist) or (None, None) if initialization fails
        """
        try:
            now = datetime.now()

            # Get or fetch sources from database/external
            sources = get_weekday_sources(self.stream_id, now.weekday())
            if not sources:
                sources = update_sources(self.external_id, self.stream_id, now.weekday(), now)
                if not sources:
                    return None, None

            # Get or fetch playlist block from database/external
            playlist = get_schedule_block(self.stream_id, now, now.hour)
            if not playlist:
                playlist = update_schedule_block(self.external_id, self.stream_id, now, now.hour)

            return sources, playlist

        except Exception as error:
            self.__logger.error(f"Failed to init schedule: {error}")
            return None, None

    @property
    def is_running(self):
        """
        Check if thread is currently running.

        :return: True if running, False otherwise
        """
        return not self.__stop_thread.is_set()

    def start(self):
        """
        Start the schedule thread and initialize schedule configuration.

        :return: Tuple (success: bool, error_message: str or None)
        """
        with self.__lock:
            # Check if stream is already active
            if self.__thread is not None and self.__thread.is_alive():
                self.__logger.warning("Schedule thread already running")
                return False, "Schedule Thread already running"

            self.__sources, self.__playlist = self.__init_schedule()

            if not self.__sources:
                return False, "Failed to initialize schedule sources"

            # Reset stop signal and create new thread
            self.__stop_thread.clear()
            self.__thread = Thread(target=self.__loop, daemon=False)
            self.__thread.start()

            self.__logger.info("Schedule thread started successfully")
            return True, None

    def stop(self):
        with self.__lock:
            # Check if stream is running
            if self.__thread is None or not self.__thread.is_alive():
                self.__logger.warning("Schedule thread not running")
                return False, "Schedule thread not running"

            # Signal thread to stop
            self.__stop_thread.set()

        # Wait for thread to finish (outside lock to avoid deadlock)
        self.__thread.join()
        self.__logger.info("Schedule thread stopped Successfully")
        return True, None

    def __loop(self):
        try:

            while not self.__stop_thread.is_set():

                self.__stop_thread.wait(10)

        except Exception as e:
            self.__logger.error(f"Schedule loop error: {e}")
            return False

        finally:
            # Cleanup resources here (close connections, files, etc.)
            self.__logger.info("schedule loop stopped")

        return True



class Transmission:
    """
    Audio stream managing encoding and broadcasting operations.
    """

    def __init__(self, stream_id: int, station_id: int, stream_name: str, external_id: int, url: str, user: str,
                 password: str, channels: int, sample_rate: int, block_size: int, bitrate: str, subjects,
                 logger: Logger = None, **kwargs):
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
        :param subjects: Audio sources
        :param logger: Logger instance
        :return: None
        """
        # Stream identifiers and configuration parameters
        self.stream_id = stream_id
        self.station_id = station_id
        self.stream_name = stream_name
        self.external_id = external_id

        # Broadcast server connection settings
        self.url = url
        self.user = user
        self.password = password

        # Audio processing parameters
        self.bitrate = bitrate
        self.channels = channels
        self.block_size = block_size
        self.sample_rate = sample_rate

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

        # Audio Sources
        self.__subjects = subjects
        self.__schedule = None

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

            while not self.__stop_stream.is_set():

                for source in self.__schedule.get_source():
                    print(source.to_dict())

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

            self.__schedule = Schedule(self.stream_id, self.external_id, self.__logger)

            success, msg = self.__schedule.start()

            if not success:
                return False, msg

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

    def __init__(self, subjects, logger: Logger = None):
        """
        Initialize station controller.

        :param subjects: Controller instance for managing subjects
        :param logger: Logger instance
        :return: None
        """
        self.__lock = Lock()
        self.__transmissions = {}
        self.__subjects = subjects
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
            transmission = Transmission(stream_name=stream_name, subjects=self.__subjects, **kwargs)

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
