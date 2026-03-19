"""
This module provides the Player class for real-time audio playback.

The Player class manages a sounddevice output stream and handles the playback
of decoded PCM audio data. It receives audio blocks in bytes format, converts
them to numpy arrays with the appropriate shape, and writes them to the configured
audio output device.

The player supports configurable sample rates, channel counts, and data types,
making it flexible for different audio stream configurations. It provides simple
start/write/stop operations for managing the playback lifecycle.

Author: Marco Graciano
Date: November 29, 2025
"""

import numpy as np
import sounddevice as sd
from .observer import Observer
from logging import Logger, getLogger


class Player(Observer):
    """
    Manages real-time audio playback from decoded PCM data.

    Handles sounddevice output stream for playing audio blocks.
    """

    def __init__(self, samplerate: int = 48000, channels: int = 2, dtype: str = 'int16', logger: Logger = None):
        """
        Initializes the Player instance.

        :param samplerate: Sample rate for audio playback (default: 48000)
        :param channels: Number of audio channels (default: 2)
        :param dtype: Data type for audio samples (default: 'int16')
        :param logger: Optional logger instance for logging operations
        """
        # Audio playback parameters
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype

        # Audio output stream for playback
        self.output = None

        # Logger instance for tracking operations
        self.logger = logger or getLogger(self.__class__.__name__)

    def start(self):
        """
        Starts the audio output stream.

        :return: Dictionary with status (bool) and message (str)
        """
        if self.output is not None:
            self.logger.warning("Player already started.")
            return {'status': False, 'message': 'Player already started.'}

        try:
            self.output = sd.OutputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype)
            self.output.start()
            return {'status': True, 'message': 'Player started successfully.'}
        except Exception as error:
            self.logger.error(f"Error starting player: {error}.")
            self.output = None
            return {'status': False, 'message': f'Error starting player: {error}.'}

    def update(self, audio_block: bytes):
        """
        Writes an audio block to the output stream.

        :param audio_block: Audio data in bytes (PCM)
        :return: None
        """
        if self.output is None:
            self.logger.error("Cannot write: player not started.")
            return

        try:
            audio_data = np.frombuffer(audio_block, dtype=np.int16).reshape(-1, self.channels)
            self.output.write(audio_data)
        except Exception as error:
            self.logger.error(f"Error writing to player: {error}")
            self.stop()

    def stop(self):
        """
        Stops the output stream and cleans up resources.

        :return: Dictionary with status (bool) and message (str)
        """
        if self.output is None:
            self.logger.warning("Player not running.")
            return {'status': False, 'message': 'Player not running.'}

        try:
            self.output.stop()
            self.output.close()
            return {'status': True, 'message': 'Player stopped successfully.'}
        except Exception as error:
            self.logger.error(f"Error stopping player: {error}.")
            return {'status': False, 'message': f'Error stopping player: {error}.'}
        finally:
            self.output = None

    def __str__(self):
        """
        Returns a string representation of the Player instance.

        :return: String representation
        """
        status = "running" if self.output is not None else "stopped"
        return f"Player(samplerate={self.samplerate}, channels={self.channels}, dtype={self.dtype}, status={status})"
