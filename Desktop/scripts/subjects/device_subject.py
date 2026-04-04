
"""
Module: dante_input.py

Author: Marco Graciano
Date: 2025-06-26

This module defines the Input class to abstract relevant information from an
audio input device. The class encapsulates important attributes (name, index,
latencies, channels, etc.) and provides getter and setter methods for each one.
This facilitates the handling of audio devices in capture or processing systems,
such as low-latency streaming workflows.
"""

import sounddevice as sd
from threading import Lock, Event
from logging import Logger, getLogger


class DeviceSubject:
    """
    Represents an audio input device.

    This class stores relevant information about the device, such as name,
    index, number of channels, and default latencies. All attributes are
    private and should be accessed through getter and setter methods.
    """

    def __init__(self, name: str, device_name: str, sample_rate: int, block_size: int, channels: int, gpi: int, gpo: int, logger: Logger = None):
        """
        Initialize audio device configuration.

        :param name: Device identifier name
        :param device_name: Physical device name
        :param sample_rate: Audio sample rate in Hz
        :param block_size: Number of frames per buffer
        :param channels: Number of audio channels
        :param gpi: General Purpose Input pin number
        :param gpo: General Purpose Output pin number
        :param logger: Optional logger instance
        """
        # Device configuration
        self.__name = name
        self.__device_name = device_name
        self.__sample_rate = sample_rate
        self.__block_size = block_size
        self.__channels = channels
        self.__gpi = gpi
        self.__gpo = gpo

        # List of active observers receiving the audio stream
        self.__observers = []

        # Thread synchronization primitives
        self.__lock = Lock()
        self.__stop_stream = Event()

        # Audio stream reference (initialized on open_input)
        self.__device_stream = None

        # Logger instance
        self.__logger = logger or getLogger(self.__name)

    @property
    def name(self) -> str:
        """
        Get device identifier name.
        """
        return self.__name

    @property
    def device_name(self) -> str:
        """
        Get physical device name.
        """
        return self.__device_name

    @property
    def sample_rate(self) -> int:
        """
        Get audio sample rate in Hz.
        """
        return self.__sample_rate

    @property
    def block_size(self) -> int:
        """
        Get the buffer block size.

        :return: Number of frames per buffer
        """
        return self.__block_size

    @property
    def channels(self) -> int:
        """
        Get the number of audio channels.

        :return: Number of channels
        """
        return self.__channels

    @property
    def gpi(self) -> int:
        """
        Get General Purpose Input pin number.
        """
        return self.__gpi

    @property
    def gpo(self) -> int:
        """
        Get General Purpose Output pin number.
        """
        return self.__gpo

    @property
    def is_active(self):
        """
        Check if generator is currently active.

        :return: True if active, False otherwise
        """
        return not self.__stop_stream.is_set()

    def attach(self, observer):
        """
        Register a new observer to receive audio blocks.

        Observers immediately start receiving the current audio stream from the moment
        of subscription.

        :param observer: Object implementing update(audio_block) method to receive numpy audio arrays
        :return: bool
        """
        with self.__lock:
            # Verify thread exists and is running
            if self.__device_stream is None:
                self.__logger.warning(f"{observer} attach rejected, generator not running")
                return False

            # Check if subject is currently active
            if not self.is_active:
                self.__logger.warning(f"{observer} attach rejected, subject is inactive")
                return False

            # Prevent duplicate observers
            if observer in self.__observers:
                self.__logger.info(f"{observer} already attached")
                return False

            # Register new observer
            self.__observers.append(observer)
            self.__logger.info(f"{observer} attached successfully")

            return True

    def detach(self, observer):
        """
        Remove a previously registered observer from the Dante stream. The observer immediately
        stops receiving audio blocks.

        :param observer: Observer instance previously registered with attach() (uses object identity)
        :return: bool
        """
        with self.__lock:
            # Verify observer is registered
            if observer not in self.__observers:
                self.__logger.warning(f"{observer} detach rejected, not found in observers")
                return False

            # Unregister observer
            self.__observers.remove(observer)
            self.__logger.info(f"{observer} detached successfully")

            return True

    def notify(self, indata, *args):
        """
        Process incoming audio data from stream.

        :param indata: Audio data array (frames x channels)
        """
        try:
            # Take snapshot of observers to avoid holding lock during notifications
            with self.__lock:
                observers_snapshot = list(self.__observers)

            # Submit each observer update to thread pool (non-blocking)
            for observer in observers_snapshot:
                observer.update(indata)

        except Exception as error:
            # Critical error in notify itself
            self.__logger.error(f"Critical error in notify method: {error}")

    @staticmethod
    def __find_device_index(device_name: str, sample_rate: int, channels: int) -> int | None:
        """
        Find device index by name, sample rate and channels.

        :param device_name: Physical device name
        :param sample_rate: Required sample rate in Hz
        :param channels: Required number of channels
        :return: Device index or None if not found
        """
        devices = sd.query_devices()

        for idx, device in enumerate(devices):
            if device['name'] == device_name and device['default_samplerate'] == sample_rate and device['max_input_channels'] >= channels:
                return idx

        return None

    def start(self, dtype: str = 'int16', latency: str = 'low'):
        """
        Start the device audio stream.

        Checks if the stream thread is already running. If not, initializes the stop event,
        creates the stream.

        :return: bool
        """
        try:
            with self.__lock:
                if self.__device_stream is not None:
                    self.__logger.warning(f"Device stream already active, cannot open new stream")
                    return False

                device_idx = self.__find_device_index(self.__device_name, self.__sample_rate, self.__channels)

                if device_idx is None:
                    self.__logger.error(f"Device not found: {self.__device_name} @ {self.__sample_rate}Hz")
                    return False

                # Configure and create input stream
                self.__device_stream = sd.InputStream(
                    dtype=dtype,
                    latency=latency,
                    device=device_idx,
                    channels=self.__channels,
                    blocksize=self.__block_size,
                    samplerate=self.__sample_rate,
                    callback=self.notify
                )

                # Start capturing audio
                self.__device_stream.start()

            # Reset stop signal for new generator
            self.__stop_stream.clear()
            self.__logger.info(f"Stream started successfully on device: {self.__device_name}")
            return True

        except Exception as error:
            self.__logger.error(f"Failed to start device stream: {error}")
            return False

    def stop(self):
        """
        Stops and closes the device audio stream if it is active.

        :return: bool
        """
        try:
            with self.__lock:
                if self.__device_stream is None:
                    self.__logger.warning(f"Device stream already stopped, nothing to close")
                    return False

                # Signal stop and close stream
                self.__stop_stream.set()
                self.__device_stream.stop()
                self.__device_stream.close()
                self.__device_stream = None

                self.__logger.info(f"Device stream stopped successfully")

                return True

        except Exception as error:
            self.__logger.error(f"Failed to stop device stream: {error}")
            return False
