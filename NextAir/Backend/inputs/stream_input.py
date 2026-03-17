"""
Module: stream_input.py

Handles HTTP audio stream connections and real-time conversion to PCM.

Autor: Marco Graciano
Date: March 16, 2026
"""

import requests
from threading import Lock
from .input_base import InputBase
from logging import Logger, getLogger


class StreamInput(InputBase):
    """
    Manages HTTP audio stream connections with configurable priority and block processing.
    Handles stream lifecycle and provides thread-safe read operations.
    """

    def __init__(self, name: str, decoder, logger: Logger = None):
        """
        Initialize the audio stream client.

        :param name: Name identifier for the logger instance
        :param decoder: LPCM streaming decoder
        :param logger: Optional logger instance, creates new if not provided
        """
        self.__name = name

        self.__lock = Lock()

        # Logger instance for tracking operations
        self.__logger = logger or getLogger(name)

        # Decoder instance for audio conversion
        self.__decoder = decoder

    @property
    def url(self) -> str:
        """
        Get stream URL.
        """
        return self.__decoder.url

    @property
    def name(self) -> str:
        """
        Get stream name.

        :return: Stream name identifier
        """
        return self.__name

    @property
    def layout(self) -> str:
        """
        Get number of audio channels.
        """
        return self.__decoder.layout

    @property
    def samplerate(self) -> int:
        """
        Get audio sample rate in Hz.
        """
        return self.__decoder.samplerate

    @property
    def output_format(self) -> str:
        """
        Get output audio format.
        """
        return self.__decoder.output_format

    def __str__(self):
        """
        String representation of decoder configuration.

        :return: Formatted decoder info
        """
        return f"stream: {self.__name}, {self.__decoder}"

    def __is_alive(self):
        """
        Check if stream URL is accessible.

        :return: True if accessible, False otherwise
        """
        try:
            response = requests.get(self.url, timeout=3, allow_redirects=True, stream=True)
            response.close()
            return response.status_code == 200
        except requests.RequestException as error:
            return False

    def open_input(self) -> bool:
        """
        Start the encoder to begin reading from stream URL.

        :return: True if opened successfully, False otherwise
        """
        with self.__lock:
            if not self.__is_alive():
                self.__logger.error(f"Stream URL not accessible: {self.url}")
                return False

            return self.__decoder.start()

    def close_input(self) -> bool:
        """
        Stop the encoder and close stream connection.

        :return: True if closed successfully, False otherwise
        """
        with self.__lock:
            return self.__decoder.stop()

    def data_generator(self):
        """
        Generate PCM audio blocks from encoder output.

        :yield: PCM audio frames
        """
        for frame in self.__decoder.data_generator():
            yield frame
