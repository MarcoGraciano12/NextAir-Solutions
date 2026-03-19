"""
Stream observer for encoder-to-broadcast transmission with automatic health monitoring.

Manages bidirectional communication between audio encoder and broadcast server through
separate threads for writing frames and reading encoded data. Includes a reload thread
that monitors encoder health and performs automatic restart on deadlock detection.

Author: Marco Graciano
Date: March 17, 2026
"""

import time
from .observer import Observer
from logging import Logger, getLogger
from threading import Thread, Lock, Event


class StreamObserver(Observer):
    """
    Observer that transmits encoded audio data to broadcast server.
    """

    def __init__(self, encoder, broadcast, reload_interval: int = 5, logger: Logger = None):
        """
        Initialize stream observer.

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

        # Logger instance for tracking operations
        self.__logger = logger or getLogger(self.__class__.__name__)

        # Thread control attributes
        self.__thread, self.__reload_thread = None, None
        self.__stop_stream, self.__lock = Event(), Lock()

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

    def __reload_loop(self):
        """
        Monitor encoder and broadcast health, restart if needed.
        """
        while not self.__stop_stream.is_set():
            self.__stop_stream.wait(self.__reload_interval)

            if self.__stop_stream.is_set():
                break

            # Check encoder health
            if not self.__encoder.is_alive:
                self.__logger.error("Encoder deadlock detected, attempting restart")
                if not self.__encoder.restart():
                    self.__logger.error("Failed to restart encoder, will retry")

            # Check broadcast health
            if not self.__broadcast.is_alive:
                self.__logger.error("Broadcast connection lost, reconnecting")
                self.__broadcast.disconnect()
                self.__broadcast.connect()

    def stop(self):
        """
        Stop transmission and monitoring threads.

        :return: True if stopped successfully, False if not running
        """
        with self.__lock:
            if not self.__thread or not self.__thread.is_alive():
                self.__logger.warning("Stream observer is not running")
                return False

            thread_to_join = self.__thread
            reload_to_join = self.__reload_thread
            self.__thread = None
            self.__reload_thread = None

        self.__stop_stream.set()

        # Wait for both threads to finish
        thread_to_join.join()
        if reload_to_join:
            reload_to_join.join()

        # Stop encoder
        self.__encoder.stop()
        # Clone connection
        self.__broadcast.disconnect()

        self.__logger.info("Stream observer stopped successfully")
        return True
