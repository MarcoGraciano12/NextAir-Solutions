"""
Module: stream_subject.py

Module for managing audio stream distribution using the Observer pattern.

Provides the AudioStreamSubject class that handles real-time audio streaming
from various input sources and distributes audio blocks to registered observers
through a background thread with thread-safe operations.

Author: Marco Graciano
Date: December 22, 2025
"""

from .subject import Subject
from logging import Logger, getLogger
from threading import Lock, Event, Thread


class StreamSubject(Subject):
    """
    Observable subject for audio streaming using the Observer pattern.

    Manages real-time audio stream reading and distributes audio blocks to
    multiple registered observers. Each observer receives live audio data
    starting from the moment they subscribe - there is no buffering of
    historical data.
    """

    def __init__(self, stream_input, logger: Logger = None):
        """
        Initializes the AudioStreamSubject instance.

        :param stream_input: StreamInput instance for reading audio data
        :param logger: Optional logger instance for logging operations
        """
        self.__observers = []  # Registered observer instances
        self.__stream_input = stream_input  # Audio data source

        self.__thread = None  # Streaming worker thread
        self.__lock = Lock()  # Protects observer list modifications
        self.__stop_event = Event()  # Signal to stop streaming thread
        self.__alive_subject = Event()  # Indicates stream is actively running

        # Logger instance for tracking operations
        self.__logger = logger or getLogger(self.stream_input.name)

    @property
    def is_alive(self):
        """
        Check if the stream is alive and running properly.

        :return: True if stream is alive, False otherwise
        """
        return self.__alive_subject.is_set()

    @property
    def stream_input(self):
        """
        StreamInput instance providing audio stream configuration and data.

        :return: StreamInput object
        """
        return self.__stream_input

    def __str__(self) -> str:
        """
        String representation of the stream subject.

        :return: Formatted string with stream subject info
        """
        return f"StreamSubject({self.__stream_input}, observers: {len(self.__observers)})"

    def attach(self, observer):
        """
        Register a new observer to receive live audio blocks.
        Observers immediately start receiving the current live audio stream from the moment
        of subscription. Unlike file-based sources, there is no buffering of historical data.

        :param observer: Object implementing update(audio_block) method to receive numpy audio arrays
        :return: dict with 'status' (bool) indicating success and 'message' (str) with details
        """
        with self.__lock:
            # Reject if stream not started
            if self.__thread is None or not self.__thread.is_alive():
                self.__logger.warning(f"Attach rejected: stream not running")
                return False

            # Reject if stream is shutting down
            if self.__stop_event.is_set():
                self.__logger.warning(f"Attach rejected: stream shutting down, observer {observer} should retry")
                return False

            # Reject if observer already registered
            if observer in self.__observers:
                self.__logger.warning(f"Attach rejected: observer {observer} already registered")
                return False

            # Add new observer to the list
            self.__observers.append(observer)

        self.__logger.info(f"Observer attached: {observer}")
        return True

    def detach(self, observer):
        """
        Remove a previously registered observer from the Dante stream.

        The observer immediately stops receiving audio blocks after removal. Unlike traditional
        implementations, this subject keeps its stream thread running continuously even when
        all observers detach, ensuring the audio input remains synchronized with the live
        Dante feed at all times.

        :param observer: Observer instance previously registered with attach() (uses object identity)
        :return: dict with 'status' (bool) indicating success and 'message' (str) with details
        """
        with self.__lock:
            # Reject if observer not registered
            if observer not in self.__observers:
                self.__logger.warning(f"Detach rejected: observer {observer} not found in registered list")
                return False

            # Remove the observer
            self.__observers.remove(observer)

        self.__logger.info(f"Observer detached: {observer}")
        return True

    def notify(self, audio_block):
        """
        Distribute audio block to all registered observers asynchronously.
        Submits each observer's update() method to a thread pool for parallel execution,
        preventing one slow or blocked observer from affecting others.

        :param audio_block: Numpy array containing audio data, typically shape (channels, samples)
        :return: None
        """
        try:
            # Take snapshot of observers to avoid holding lock during notifications
            with self.__lock:
                observers_snapshot = list(self.__observers)

            # Submit each observer update to thread pool (non-blocking)
            for observer in observers_snapshot:
                observer.update(audio_block)

        except Exception as error:
            # Critical error in notify itself (very rare)
            self.__logger.error(f"Critical error in notify method: {error}")

    def start(self):
        """
        Start the audio stream in a separate background thread.

        Checks if the stream thread is already running. If not, initializes the stop event,
        creates the stream thread, and starts the stream processing loop asynchronously.

        :return: bool
        """
        with self.__lock:
            if self.__thread and self.__thread.is_alive():
                self.__logger.warning("Subject already running")
                return False

            self.__stop_event.clear()
            self.__alive_subject.clear()
            self.__thread = Thread(target=self.__loop, daemon=True)
            self.__thread.start()

        if self.__alive_subject.wait(timeout=0.5):
            self.__logger.info("Stream thread started successfully")
            return True

        self.__logger.warning("Thread start with timeout")
        return False

    def __loop(self):
        """
        Main loop for receiving and distributing audio blocks.

        This method runs in a background thread and performs the following operations:
        - Opens the audio input stream
        - Continuously reads audio blocks via generator
        - Distributes each block to all registered observers
        - Handles graceful shutdown on stop signal or errors

        :return: None
        """
        try:
            # Open and initialize audio stream with configured parameters
            if not self.stream_input.open_input():
                return

            self.__alive_subject.set()

            # Create audio block generator for continuous reading
            generator = self.stream_input.data_generator()

            # Process audio blocks continuously until stop signal received
            for block in generator:
                self.notify(block)

        except Exception as error:
            self.__logger.error(f"Critical exception in stream loop: {error}")

        finally:
            self.__alive_subject.clear()
            self.__logger.info("Stream thread terminated and cleaned up")

    def stop_stream(self):
        """
        Stop the audio stream thread gracefully.

        Signals the stream thread to stop and waits for it to terminate. This method
        is called when the last observer detaches. Must be called without holding the
        main lock to avoid deadlocks during the cleanup phase.

        :return: bool
        """
        with self.__lock:
            # Validate thread is running
            if not self.__thread or not self.__thread.is_alive():
                self.__logger.warning("No active thread to stop")
                return False

            # Signal thread to stop
            self.__stream_input.close_input()
            thread_to_join = self.__thread

            # Wait for thread completion (inside lock prevents concurrent start)
            thread_to_join.join()
            self.__thread = None

        self.__logger.info("Stream thread stopped successfully")
        return True
