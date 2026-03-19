"""
Module: ogg.py

FFmpeg subprocess wrapper for LPCM to OGG Opus encoding.

Author: Marco Graciano
Date: March 18, 2026
"""

import subprocess
from time import monotonic
from threading import Event
from logging import Logger, getLogger


class OGG:
    """
    Manages FFmpeg subprocess for real-time LPCM to OGG Opus encoding.
    """

    def __init__(self, name: str, channels: int, sample_rate: int, block_size: int, bitrate: str, logger: Logger = None):
        """
        Initialize the OGG encoder with audio parameters.

        :param name: Identifier for this encoder instance
        :param channels: Number of audio channels (1=mono, 2=stereo)
        :param sample_rate: Sample rate in Hz (e.g., 48000)
        :param block_size: Buffer size in samples
        :param bitrate: Target bitrate for Opus (e.g., '128k')
        :param logger: Logger instance for tracking operations
        """
        self.__channels = channels
        self.__bitrate = bitrate
        self.__sample_rate = sample_rate
        self.__block_size = block_size

        # Control flag for subprocess lifecycle
        self.__stop_event = Event()
        self.__stop_event.set()

        # Timestamp for read/write deadlock detection
        self.__last_read = monotonic()
        self.__last_write = monotonic()

        # FFmpeg subprocess handle
        self.__subprocess = None

        self.__name = name or self.__class__.__name__
        self.__logger = logger or getLogger(self.__name)

    @property
    def name(self) -> str:
        """
        Get encoder instance name.
        """
        return self.__name

    @property
    def channels(self) -> int:
        """
        Get number of audio channels.
        """
        return self.__channels

    @property
    def sample_rate(self) -> int:
        """
        Get sample rate in Hz.
        """
        return self.__sample_rate

    @property
    def block_size(self) -> int:
        """
        Get buffer size in samples.
        """
        return self.__block_size

    @property
    def bitrate(self) -> str:
        """
        Get target bitrate for encoding.
        """
        return self.__bitrate

    @property
    def is_alive(self) -> bool:
        """
        Check if FFmpeg subprocess is active and responsive.
        """
        if self.__subprocess is None:
            return False

        now = monotonic()
        write_alive = (now - self.__last_write) < 3.0
        read_alive = (now - self.__last_read) < 3.0

        return write_alive and read_alive

    def __str__(self) -> str:
        """
        Return string representation of encoder configuration.
        """
        return (
            f"name: {self.__name}, "
            f"codec: libopus, "
            f"container: ogg, "
            f"channels: {self.__channels}, "
            f"sample_rate: {self.__sample_rate}, "
            f"block_size: {self.__block_size}, "
            f"bitrate: {self.__bitrate}"
        )

    def build_command(self):
        """
        Build FFmpeg command for LPCM to OGG Opus encoding.

        :return: List of command arguments for subprocess execution
        """
        return [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-nostats",
            "-threads", "1",

            # input: raw PCM from stdin
            "-f", "s16le",
            "-ar", str(self.__sample_rate),
            "-ac", str(self.__channels),
            "-i", "pipe:0",

            # disable unused streams
            "-vn",
            "-sn",
            "-dn",

            # audio encode
            "-c:a", "libopus",
            "-b:a", self.__bitrate,  # e.g. "64k", "96k", "128k"
            "-vbr", "on",  # or "off" if you want stricter rate
            "-application", "audio",  # or "voip" for speech
            "-compression_level", "10",

            # container
            "-f", "ogg",
            "pipe:1",
        ]

    @property
    def is_running(self) -> bool:
        """
        Check if FFmpeg process is still active.

        :return: True if process is running, False otherwise
        """
        return not self.__stop_event.is_set()

    def write(self, block: bytes) -> bool:
        """
        Write LPCM data to FFmpeg stdin.

        :param block: Raw audio data
        :return: True if successful, False otherwise
        """
        if self.__stop_event.is_set():
            self.__logger.warning("Write failed ffmpeg is not active")
            return False

        try:
            self.__subprocess.stdin.write(block)
            self.__subprocess.stdin.flush()
            self.__last_write = monotonic()
            return True
        except (BrokenPipeError, ValueError):
            self.__logger.error("Broken pipe or stdin closed in FFmpeg")
            self.stop()
            return False
        except Exception as error:
            self.__logger.error(f"Error writing to FFmpeg: {str(error)}")
            self.stop()
            return False

    def read(self) -> bytes:
        """
        Read encoded data from FFmpeg stdout.

        :return: Data read or empty if fails
        """
        if self.__stop_event.is_set():
            return b''

        try:
            # Read encoded data from FFmpeg stdout
            data = self.__subprocess.stdout.read(self.__block_size)

            # Return empty if no data available (EOF or no output yet)
            if not data:
                return b''

            # Update activity timestamp on successful read
            self.__last_read = monotonic()

            return data

        except Exception as error:
            self.__subprocess.error(f"Error reading from FFmpeg: {str(error)}")
            self.stop()
            return b''

    def start(self) -> bool:
        """
        Start FFmpeg decoding process.

        :return: True if started successfully, False if already running or failed
        """
        if not self.__stop_event.is_set():
            self.__logger.warning("Encoder already running")
            return False

        try:
            self.__subprocess = subprocess.Popen(
                self.build_command(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0
            )
            self.__stop_event.clear()
            self.__logger.info(f"FFmpeg {self.__name} encoder started")
            return True

        except FileNotFoundError:
            self.__logger.error("FFmpeg not found. Install it first")
            return False
        except Exception as error:
            self.__logger.error(f"Failed to start encoder: {error}")
            return False

    def stop(self) -> bool | None:
        """
        Stop FFmpeg encoding process by force kill.

        :return: True if stopped successfully, False if not running
        """
        if self.__stop_event.is_set():
            self.__logger.warning("Encoder not running")
            return False

        try:
            self.__stop_event.set()
            self.__subprocess.kill()
            self.__subprocess.wait()
            self.__logger.info("FFmpeg encoder stopped")
            return True

        except Exception as e:
            self.__logger.error(f"Error stopping encoder: {e}")
            return False

        finally:
            self.__subprocess = None

    def restart(self) -> bool:
        """
        Restart FFmpeg subprocess (stop and start).

        :return: True if restarted successfully, False otherwise
        """
        self.__logger.warning("Restarting FFmpeg encoder")

        # Stop current process if running
        self.stop()

        # Start new process
        if self.start():
            self.__logger.info("FFmpeg encoder restarted successfully")
            return True

        self.__logger.error("Failed to restart FFmpeg encoder")
        return False
