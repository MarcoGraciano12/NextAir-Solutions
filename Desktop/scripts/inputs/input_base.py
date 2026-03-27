"""
Module: input_base.py

Defines the base interface for input sources with data generation.

Author: Marco Graciano
Date: 2026-03-12
"""

from abc import ABC, abstractmethod


class InputBase(ABC):
    """
    Base interface for input sources that generate data streams.
    """

    @abstractmethod
    def open_input(self, *args, **kwargs):
        """
        Opens and initializes the input source.

        :param args: Positional arguments for input configuration
        :param kwargs: Keyword arguments for input configuration
        :return: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def data_generator(self, *args, **kwargs):
        """
        Generator that yields data from the input source.

        :param args: Positional arguments for generator configuration
        :param kwargs: Keyword arguments for generator configuration
        :return: Generator yielding data chunks
        """
        pass

    @abstractmethod
    def close_input(self):
        """
        Closes and releases the input source.

        :return: True if successful, False otherwise
        """
        pass
