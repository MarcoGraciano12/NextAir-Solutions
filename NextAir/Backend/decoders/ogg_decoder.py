"""
Module: ogg_decoder.py

OGG to LPCM streaming decoder with configurable audio parameters.

Autor: Marco Graciano
Date: March 16, 2026
"""

import av
from threading import Event
from logging import Logger, getLogger


class OGGDecoder:
    """
    Converts OGG audio streams to Linear PCM format in real-time.
    """

    def __init__(self, url: str, layout: str, samplerate: int, output_format: str = "s16", logger: Logger = None):
        """
        Initialize OGG decoder with target audio specifications.

        :param url: HTTP stream URL
        :param layout: Audio channel layout (mono, stereo)
        :param samplerate: Target sample rate in Hz
        :param output_format: PCM format (s16, s24, s32)
        :param logger: Logger instance
        """
        # Stream configuration
        self.__url = url

        # Audio configuration
        self.__layout = layout
        self.__samplerate = samplerate

        # Format configuration
        self.__output_format = output_format

        # Signal to stop decoding
        self.__close_input = Event()
        self.__close_input.set()    # Init event

        # Logger instance for tracking operations
        self.__logger = logger or getLogger(self.__class__.__name__)

    @property
    def url(self) -> str:
        """
        Get stream URL.
        """
        return self.__url

    @property
    def layout(self) -> str:
        """
        Get number of audio channels.
        """
        return self.__layout

    @property
    def samplerate(self) -> int:
        """
        Get audio sample rate in Hz.
        """
        return self.__samplerate

    @property
    def output_format(self) -> str:
        """
        Get output audio format.
        """
        return self.__output_format

    def is_running(self):
        """
        Check if decoder is active.

        :return: True if decoder is running, False otherwise
        """
        return not self.__close_input.is_set()

    def __str__(self):
        """
        String representation of decoder configuration.

        :return: Formatted decoder info
        """
        status = "running" if self.is_running() else "stopped"
        return (f"decoder: ogg, url: {self.__url}, layout: {self.__layout}, "
                f"samplerate: {self.__samplerate}Hz, format: {self.__output_format}, status: {status}")

    def start(self):
        """
        Reset stop signal to allow decoding.

        :return: None
        """
        self.__close_input.clear()
        return True

    def stop(self):
        """
        Signal decoder to stop processing stream.

        :return: None
        """
        self.__close_input.set()
        return True

    def data_generator(self):
        """
        Generate resampled audio frames from OGG stream.

        :return: Generator yielding LPCM frames
        """
        # Open stream with auto-reconnect on network failures
        container = av.open(self.__url, options={'reconnect': '1'})

        # Configure audio resampler to target format
        resampler = av.AudioResampler(format=self.__output_format, layout=self.__layout, rate=self.__samplerate)

        try:
            # Decode frames from audio stream
            for frame in container.decode(audio=0):
                # Check for stop signal
                if self.__close_input.is_set():
                    self.__logger.info("Stop decoder signal received")
                    break

                # Resample and yield each frame
                for resampled_frame in resampler.resample(frame):
                    yield resampled_frame.to_ndarray()

        except Exception as error:
            self.__logger.error(f"Stream failed: {error}")

        finally:
            # Always close container to release resources
            container.close()
