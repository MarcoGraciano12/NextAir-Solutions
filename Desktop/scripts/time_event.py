"""
Time event module for managing timed and signal-based waiting.

This module provides the TimeEvent class which allows threads to wait for
a specified duration or indefinitely until notified by another thread.

Author: Marco Graciano
Date: October 15, 2025
"""

from threading import Event


class TimeEvent:
    """
    Event handler that can wait for a specified duration or indefinitely until notified.

    This class uses threading.Event internally to provide efficient thread synchronization
    with minimal latency. It supports both timed waits and indefinite waits that can be
    interrupted by external notifications.
    """

    def __init__(self):
        """
        Initialize the TimeEvent.
        """
        self.event = Event()

    def wait_for(self, duration: float):
        """
        Wait for a specified duration or until notified.

        :param duration: Time to wait in seconds.
        :return: Dictionary with status (True if timeout, False if notified) and message.
        """
        self.event.clear()  # Reset event before waiting

        self.event.wait(timeout=duration)

    def wait(self):
        """
        Wait indefinitely until notified.

        :return: Dictionary with status and message.
        """
        self.event.clear()  # Reset event before waiting

        self.event.wait()

    def notify(self):
        """
        Wake up the waiting event.

        :return: None
        """
        self.event.set()
