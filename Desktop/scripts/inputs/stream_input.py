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

    def __init__(self, name: str, decoder, logger: Logger = None, *kwargs):
        """
        Initialize the audio stream client.

        :param name: Name identifier for the logger instance
        :param decoder: LPCM streaming decoder
        :param logger: Optional logger instance, creates new if not provided
        """
        self.__lock = Lock()

        # Decoder instance for audio conversion
        self.__decoder = decoder

        self.__name = name or self.__class__.__name__
        # Logger instance for tracking operations
        self.__logger = logger or getLogger(self.__name)

    @property
    def url(self) -> str:
        """
        Get stream URL.
        """
        return self.__decoder.url

    @property
    def name(self) -> str:
        """
        Get input name.

        :return: Stream name identifier
        """
        return self.__name

    @property
    def decoder_name(self) -> str:
        """
        Get decoder name.

        :return: Stream name identifier
        """
        return self.__decoder.name

    @property
    def channels(self) -> str:
        """
        Get number of audio channels.
        """
        return self.__decoder.channels

    @property
    def sample_rate(self) -> int:
        """
        Get audio sample rate in Hz.
        """
        return self.__decoder.sample_rate

    @property
    def block_size(self) -> str:
        """
        Get block size.
        """
        return self.__decoder.block_size

    def __str__(self):
        """
        String representation of decoder configuration.

        :return: Formatted decoder info
        """
        return f"input_name: {self.__name}, {self.__decoder}"

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
        try:
            while True:
                block = self.__decoder.read()

                if not block:
                    return

                yield block
        except (BrokenPipeError, IOError, OSError) as error:
            self.__logger.error(f"Pipe error in audio generator: {error}")
            self.close_input()
            return
