"""
DeviceInput controller for CRUD operations.

Author: Marco Graciano
Date: 2025-03-26

Handles database operations for DeviceInput model.
"""

from db import engine
from models import DeviceInput
from sqlalchemy.orm import Session
from logging import Logger, getLogger


class DeviceInputController:
    """
    Controller for DeviceInput CRUD operations.

    Manages database transactions for DeviceInput entities.
    Each method creates and closes its own session.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize DeviceInputController.

        :param logger: Logger instance for logging operations
        """
        self.__logger = logger or getLogger(self.__class__.__name__)

    def create(self, name: str, device_name: str, sample_rate: int, block_size: int, channels: int, gpi: int, gpo: int):
        """
        Creates a new audio input device configuration.

        :param name: Unique identifier for the device
        :param device_name: Physical device name from the OS
        :param sample_rate: Audio sample rate in Hz
        :param block_size: Audio block size in frames
        :param channels: 1 for mono, 2 for stereo
        :param gpi: General Purpose Input pin number
        :param gpo: General Purpose Output pin number
        :return: Tuple (success: bool, result: DeviceInput or error message)
        """
        try:
            with Session(engine) as session:
                # Check if name exist
                if session.query(DeviceInput).filter_by(name=name).first():
                    return False, f"Name already exists: {name}"

                # Check if device_name exist
                if session.query(DeviceInput).filter_by(device_name=device_name).first():
                    return False, f"Device name already exists: {device_name}"

                device_input = DeviceInput(
                    name=name,
                    device_name=device_name,
                    sample_rate=sample_rate,
                    block_size=block_size,
                    channels=channels,
                    gpi=gpi,
                    gpo=gpo
                )
                session.add(device_input)
                session.commit()
                session.refresh(device_input)

                return True, device_input

        except Exception as error:
            self.__logger.error(f"Error creating device input: {error}")
            return False, "Error creating device input"

    def delete(self, name: str):
        """
        Deletes an audio input device by name.

        :param name: ID of the device to delete
        :return: Tuple (success: bool, message: str)
        """
        try:
            with Session(engine) as session:
                # Check if device input exists
                device_input = session.query(DeviceInput).filter_by(name=name).first()

                if not device_input:
                    return False, f"Device Input not found: {name}"

                session.delete(device_input)
                session.commit()

                return True, device_input

        except Exception as error:
            self.__logger.error(f"Error deleting device input: {error}")
            return False, "Error deleting device input"

    def get(self, device_input_id: int):
        """
        Get device input by ID.

        :param device_input_id: StreamInput primary key
        :return: Tuple (success: bool, result: DeviceInput or error message)
        """
        try:
            with Session(engine) as session:
                device_input = session.query(DeviceInput).filter_by(id=device_input_id).first()

                if not device_input:
                    return False, f"Device Input not found: {device_input_id}"

            return True, device_input

        except Exception as error:
            self.__logger.error(f"Error retrieving device input: {error}")
            return False, "Error retrieving device input"

    def get_all(self):
        """
        Get all device inputs.

        :return: Tuple (success: bool, result: list of DeviceInputs or error message)
        """
        try:
            with Session(engine) as session:
                device_inputs = session.query(DeviceInput).all()

                return device_inputs

        except Exception as error:
            self.__logger.error(f"Error retrieving device inputs: {error}")
            return None

    def get_by_name(self, name: str):
        """
        Get device input by name.

        :param name: Name to search
        :return: Tuple (success: bool, result: DeviceInput or error message)
        """
        try:
            with Session(engine) as session:
                device_input = session.query(DeviceInput).filter_by(name=name).first()

                if not device_input:
                    return False, f"Device Input not found: {name}"

            return True, device_input

        except Exception as error:
            self.__logger.error(f"Error searching device input: {error}")
            return False, "Error searching device input"

    def update(self, device_input_id: int, **kwargs):
        """

        :param device_input_id:
        :param kwargs:
        :return:
        """
        try:
            with Session(engine) as session:
                # Check if device input exists
                device_input = session.query(DeviceInput).filter_by(id=device_input_id).first()

                if not device_input:
                    return False, F"Device Input not found: {device_input_id}"

                # If updating name, check it doesn't exist for another input
                if "name" in kwargs:
                    exists = session.query(DeviceInput).filter_by(name=kwargs["name"]).first()

                    if exists and exists.id != device_input_id:
                        return False, f"Name already exists: {kwargs['name']}"

                # If updating device_name, check it doesn't exist for another input
                if "device_name" in kwargs:
                    exists = session.query(DeviceInput).filter_by(device_name=kwargs["device_name"]).first()

                    if exists and exists.id != device_input_id:
                        return False, f"Device name already exists: {kwargs['device_name']}"

                # Update fields
                for key, value in kwargs.items():
                    if hasattr(device_input, key):
                        setattr(device_input, key, value)

                session.commit()
                session.refresh(device_input)

                return True, device_input

        except Exception as error:
            self.__logger.error(f"Error updating device input: {error}")
            return False, "Error updating device input"

    def search_by_name(self, search_term: str):
        """
        Search device inputs by name using partial matching.

        :param search_term: Text to search in device input names (case-insensitive)
        :return: Tuple (success: bool, device_inputs: list[DeviceInput] or error message)
        """
        try:
            with Session(engine) as session:
                # Use ilike for case-insensitive partial matching
                device_inputs = session.query(DeviceInput).filter(DeviceInput.name.ilike(f"%{search_term}%")).all()

                if not device_inputs:
                    return False, f"No device inputs found matching: {search_term}"

                return True, device_inputs

        except Exception as error:
            self.__logger.error(f"Error searching device inputs: {error}")
            return False, "Error searching device inputs"
