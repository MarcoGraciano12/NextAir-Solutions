"""
Module: decoder.py

LPCM streaming decoder with configurable audio parameters.

Autor: Marco Graciano
Date: March 16, 2026
"""

import subprocess
from logging import Logger, getLogger


class Decoder:
    """
    Converts audio streams to Linear PCM format in real-time.
    """

    def __init__(self,name: str, url: str, channels: int, sample_rate: int, block_size: int, logger: Logger = None):
        """
        Initialize decoder with target audio specifications.

        :param url: HTTP stream URL
        :param channels: Number of channels
        :param sample_rate: Target sample rate in Hz
        :param block_size:  Size of each audio block to read in bytes
        :param logger: Logger instance
        """
        # Stream configuration
        self.__url = url

        # Audio configuration
        self.__channels = channels
        self.__block_size = block_size
        self.__sample_rate = sample_rate

        # FFmpeg subprocess
        self.__subprocess = None

        self.__name = name or self.__class__.__name__
        # Logger instance for tracking operations
        self.__logger = logger or getLogger(self.__name)

    @property
    def name(self) -> str:
        """
        Get stream name.

        :return: Stream name identifier
        """
        return self.__name

    @property
    def url(self) -> str:
        """
        Get stream URL.
        """
        return self.__url

    @property
    def channels(self) -> int:
        """
        Get number of audio channels.
        """
        return self.__channels

    @property
    def sample_rate(self) -> int:
        """
        Get audio sample rate in Hz.
        """
        return self.__sample_rate

    @property
    def block_size(self) -> int:
        """
        Get configured frame size.

        :return: Number of samples per frame
        """
        return self.__block_size

    def __str__(self):
        """
        String representation of decoder configuration.

        :return: Formatted decoder info
        """
        return (
            f"url: {self.__url}, channels: {self.__channels}, sample_rate: {self.__sample_rate}Hz, "
            f"block_size: {self.__block_size}, sample_fmt: s16le, codec: pcm_s16le"
        )

    def build_command(self) -> list:
        """
        Build FFmpeg command reading directly from stream URL.

        :return: FFmpeg command as list
        """
        cmd = [
            "ffmpeg",
            "-rw_timeout", "5000000",

            # Reduce logs
            "-loglevel", "error",
            "-nostats",
            "-hide_banner",

            # Limit threads
            "-threads", "1",

            # Reduce probing (optional, cuidado)
            "-probesize", "32k",
            "-analyzeduration", "0",

            # Input
            "-i", self.__url,

            # Disable unused streams
            "-vn",
            "-sn",
            "-dn",

            # Output raw PCM
            "-f", "s16le",
            "-acodec", "pcm_s16le",
            "-ar", str(self.__sample_rate),
            "-ac", str(self.__channels),

            # Output pipe
            "pipe:1"
        ]

        return cmd

    def is_running(self) -> bool:
        """
        Check if FFmpeg process is still active.

        :return: True if process is running, False otherwise
        """
        return self.__subprocess is not None

    def start(self) -> bool:
        """
        Start FFmpeg encoding process.

        :return: True if started successfully, False if already running or failed
        """
        if self.is_running():
            self.__logger.warning("Encoder already running")
            return False

        try:
            self.__subprocess = subprocess.Popen(
                self.build_command(),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            self.__logger.info(f"FFmpeg encoder started for {self.__url}")
            return True

        except FileNotFoundError:
            self.__logger.error("FFmpeg not found. Install it first")
            return False
        except Exception as e:
            self.__logger.error(f"Failed to start encoder: {e}")
            return False

    def stop(self) -> bool:
        """
        Stop FFmpeg encoding process by force kill.

        :return: True if stopped successfully, False if not running
        """
        if not self.is_running():
            self.__logger.warning("Encoder not running")
            return False

        try:
            self.__subprocess.kill()
            self.__subprocess.wait()
            self.__logger.info("FFmpeg encoder stopped")

        except Exception as e:
            self.__logger.error(f"Error stopping encoder: {e}")
            return False

        finally:
            self.__subprocess = None

            return True

    def read(self) -> bytes:
        """
        Read encoded audio data from FFmpeg output.

        :param size: Number of bytes to read
        :return: Encoded audio bytes or empty bytes if no data
        """
        if not self.is_running():
            return b''

        data = self.__subprocess.stdout.read1(self.__block_size)
        return data if data else b''
