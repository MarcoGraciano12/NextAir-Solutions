"""
Stream observer for encoder-to-broadcast transmission with automatic health monitoring.

Manages bidirectional communication between audio encoder and broadcast server through
separate threads for writing frames and reading encoded data. Includes a reload thread
that monitors encoder health and performs automatic restart on deadlock detection.

Author: Marco Graciano
Date: March 17, 2026
"""

import time
from email.feedparser import NeedMoreData

from .observer import Observer
from logging import Logger, getLogger
from threading import Thread, Lock, Event


class StreamObserver(Observer):
    """
    Observer that transmits encoded audio data to broadcast server.
    """

    def __init__(self, name: str, encoder = None, broadcast = None, reload_interval: int = 5, logger: Logger = None):
        """
        Initialize stream observer.

        :param name: Identifier for this observer instance
        :param encoder: Audio encoder instance
        :param broadcast: broadcast transmitter instance
        :param reload_interval: Seconds between encoder health checks
        :param logger: Logger instance
        """
        # Encoder and transmitter instances
        self.__encoder = encoder
        self.__broadcast = broadcast

        # Reload monitoring interval
        self.__reload_interval = reload_interval

        # Thread control attributes
        self.__thread, self.__reload_thread = None, None
        self.__stop_stream, self.__lock = Event(), Lock()

        # Logger instance for tracking operations
        self.__name = name or self.__class__.__name__
        self.__logger = logger or getLogger(self.__name)

    @property
    def name(self) -> str:
        """
        Get observer instance name.
        """
        return self.__name

    @property
    def encoder(self):
        """
        Get encoder instance
        :return: Encoder object
        """
        return self.__encoder

    @encoder.setter
    def encoder(self, value):
        """
        Set encoder instance
        :param value: Encoder object
        """
        self.__encoder = value

    @property
    def broadcast(self):
        """
        Get broadcast instance
        :return: Broadcast object
        """
        return self.__broadcast

    @broadcast.setter
    def broadcast(self, value):
        """
        Set broadcast instance
        :param value: Broadcast object
        """
        self.__broadcast = value

    @property
    def logger(self):
        """
        Get logger instance
        :return: Logger object
        """
        return self.__logger

    def __str__(self):
        """
        String representation of the stream observer.

        :return: Formatted string with stream observer info
        """
        return self.__name

    def update(self, frame):
        """
        Receive audio frame from subject and write to encoder.

        :param frame: AudioFrame to encode
        :return: True if frame written successfully, False if observer stopped
        """
        if self.__stop_stream.is_set():
            return False

        self.__encoder.write(frame)
        return True

    def start(self):
        """
        Start transmission and monitoring threads.

        :return: True if started successfully, False if already running
        """
        with self.__lock:
            if (self.__thread and self.__thread.is_alive()) or \
                    (self.__reload_thread and self.__reload_thread.is_alive()):
                self.__logger.warning("Stream observer already running")
                return False

            # Start encoder
            if not self.__encoder.start():
                return False

            if not self.__broadcast.connect():
                self.__encoder.stop()
                return False

            self.__stop_stream.clear()

            # Start sender thread
            self.__thread = Thread(target=self.__sender_loop, daemon=True)
            self.__thread.start()

            # Start reload monitoring thread
            self.__reload_thread = Thread(target=self.__reload_loop, daemon=True)
            self.__reload_thread.start()

            self.__logger.info("Stream observer started")
            return True

    def __sender_loop(self):
        """
        Continuous loop that reads from encoder and sends to broadcast.
        """
        while not self.__stop_stream.is_set():
            data = self.__encoder.read()

            if not data:
                self.__logger.warning("No data available from encoder")
                time.sleep(0.001)
                continue

            # Just try to send, reload_loop handles reconnection
            self.__broadcast.send(data)
            time.sleep(0.001)

    def restart_encoder(self) -> bool:
        """
        Attempt to restart the encoder.

        :return: True if restarted successfully, False otherwise
        """
        self.__logger.error("Encoder deadlock detected, attempting restart")

        if not self.__encoder.restart():
            self.__logger.error("Failed to restart encoder, will retry")
            return False

        return True

    def restart_broadcast(self) -> bool:
        """
        Restart broadcast connection with fresh encoder state.

        :return: True if reconnected successfully, False otherwise
        """
        self.__logger.error("Broadcast connection lost, restarting encoder and reconnecting")

        # Close existing broadcast connection
        self.__broadcast.disconnect()

        # Restart encoder to ensure OGG stream starts from valid page boundary
        if not self.__encoder.restart():
            self.__logger.error("Failed to restart encoder")
            return False

        # Reconnect to broadcast server
        if not self.__broadcast.connect():
            self.__logger.error("Failed to reconnect to broadcast")
            return False

        self.__logger.info("Broadcast reconnected with fresh encoder")
        return True

    def __reload_loop(self):
        """
        Monitor encoder and broadcast health, restart if needed.
        """
        while not self.__stop_stream.is_set():
            # Wait for interval or stop signal
            self.__stop_stream.wait(self.__reload_interval)

            if self.__stop_stream.is_set():
                break

            # Check encoder health
            if not self.__encoder.is_alive:
                self.restart_encoder()

            # Check broadcast health
            if not self.__broadcast.is_alive:
                self.restart_broadcast()

    def stop(self):
        """
        Stop transmission and monitoring threads.

        :return: True if stopped successfully, False if not running
        """
        with self.__lock:
            if not self.__thread or not self.__thread.is_alive():
                self.__logger.warning("Stream observer is not running")
                return False

            # Stop encoder
            self.__encoder.stop()

            # Clone connection
            self.__broadcast.disconnect()

            self.__stop_stream.set()

            thread_to_join = self.__thread
            reload_to_join = self.__reload_thread

            self.__thread = None
            self.__reload_thread = None

        # Wait for both threads to finish
        thread_to_join.join()

        if reload_to_join:
            reload_to_join.join()

        self.__logger.info("Stream observer stopped successfully")
        return True
