"""
Module: subject.py

Defines the Subject interface for the Observer pattern.

Author: Marco Graciano
Date: 2025-07-04
"""

from abc import ABC, abstractmethod


class Subject(ABC):
    """
    Subject interface that defines the observable contract.
    """

    @abstractmethod
    def attach(self, observer) -> None:
        """
        Attaches an observer to the subject.

        :param observer: The observer to attach
        :return: None
        """
        pass

    @abstractmethod
    def detach(self, observer) -> None:
        """
        Detaches an observer from the subject.

        :param observer: The observer to detach
        :return: None
        """
        pass

    def notify(self, *args, **kwargs) -> None:
        """
        Notifies all attached observers with optional data.

        :param args: Positional arguments to pass to observers
        :param kwargs: Keyword arguments to pass to observers
        :return: None
        """
        pass

    def __str__(self):
        """
        Returns the class name for logging and debugging purposes.

        :return: String representation of the subject
        """
        return f"{self.__class__.__name__}"
