"""
Device Inputs ORM model.

Author: Marco Graciano
Date: 2025-03-26

Represents an audio input source configuration.
"""

from db import Base
from sqlalchemy import Column, Integer, String


class DeviceInput(Base):
    """
    Audio input device configuration for sound capture.

    Represents physical audio devices accessible via sounddevice library.
    Stores device parameters and GPIO pin assignments for hardware control.

    :param id: Primary key
    :param name: Unique identifier for the input device
    :param device_name: Physical device name as recognized by the OS
    :param sample_rate: Audio sample rate in Hz (e.g., 44100, 48000)
    :param gpi: General Purpose Input pin number
    :param gpio: General Purpose Output pin number
    """
    __tablename__ = 'device_inputs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    device_name = Column(String(255), unique=True, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    gpi = Column(Integer, nullable=True)
    gpo = Column(Integer, nullable=True)


    def to_dict(self) -> dict:
        """
        Converts device input instance to dictionary.

        :return: Dictionary with all device attributes
        """
        return {
            'id': self.id,
            'name': self.name,
            'device_name': self.device_name,
            'sample_rate': self.sample_rate,
            'gpi': self.gpi,
            'gpio': self.gpio
        }
