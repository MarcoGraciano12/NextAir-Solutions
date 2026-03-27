"""
Module: observer.py

Defines the Observer interface for the Observer pattern.

Author: Marco Graciano
Date: 2025-07-04
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Observer interface that defines the update contract.
    """

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """
        Receives updates from the subject.

        :param args: Positional arguments from subject
        :param kwargs: Keyword arguments from subject
        :return: None
        """
        pass

    def __str__(self):
        """
        Returns the class name for logging and debugging purposes.

        :return: String representation of the observer
        """
        return f"{self.__class__.__name__}"
