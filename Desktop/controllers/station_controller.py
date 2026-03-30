"""
Station controller for CRUD operations.

Author: Marco
Date: 2025-03-26
Handles database operations for Station model.
"""

from db import engine
from models import Station
from sqlalchemy.orm import Session
from logging import Logger, getLogger


class StationController:
    """
    Controller for Station CRUD operations.

    Manages database transactions for Station entities.
    Each method creates and closes its own session.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize StationController.

        :param logger: Logger instance for logging operations
        """
        self.__logger = logger or getLogger(self.__class__.__name__)

    def create(self, station_name: str, files_path: str):
        """
        Create a new station.

        :param station_name: Unique station name
        :param files_path: File system path for station files
        :return: Tuple (success: bool, result: Station or error message)
        """
        try:
            with Session(engine) as session:
                # Check if name exists within same transaction
                if session.query(Station).filter_by(station_name=station_name).first():
                    return False, f"Station already exists: {station_name}"

                station = Station(station_name=station_name, files_path=files_path)
                session.add(station)
                session.commit()
                session.refresh(station)

                return True, station

        except Exception as e:
            self.__logger.error(f"Error creating station: {e}")
            return False, "Error creating station"

    def get(self, station_id: int):
        """
        Get station by ID.

        :param station_id: Station primary key
        :return: Tuple (success: bool, result: Station or error message)
        """
        try:
            with Session(engine) as session:
                station = session.query(Station).filter_by(station_id=station_id).first()

                if not station:
                    return False, f"Station not found: {station_id}"

                return True, station

        except Exception as e:
            self.__logger.error(f"Error retrieving station: {e}")
            return False, "Error retrieving station"

    def get_all(self):
        """
        Get all stations.

        :return: List of Stations or None
        """
        try:
            with Session(engine) as session:
                stations = session.query(Station).all()
                return stations

        except Exception as e:
            self.__logger.error(f"Error retrieving stations: {e}")
            return None

    def get_by_name(self, station_name: str):
        """
        Get station by name.

        :param station_name: Station name to search
        :return: Tuple (success: bool, result: Station or error message)
        """
        try:
            with Session(engine) as session:
                station = session.query(Station).filter_by(station_name=station_name).first()

                if not station:
                    return False, f"Station not found: {station_name}"

                return True, station

        except Exception as e:
            self.__logger.error(f"Error searching station: {e}")
            return False, "Error searching station"

    def delete(self, station_id: int):
        """
        Delete station by ID.

        :param station_id: Station primary key
        :return: Tuple (success: bool, result: success message or error message)
        """
        try:
            with Session(engine) as session:
                # Check if station exists
                station = session.query(Station).filter_by(station_id=station_id).first()

                if not station:
                    return False, f"Station not found: {station_id}"

                station_name = station.station_name
                session.delete(station)
                session.commit()

                return True, f"Station deleted: {station_name}"

        except Exception as e:
            self.__logger.error(f"Error deleting station: {e}")
            return False, "Error deleting station"

    def update(self, station_id: int, **kwargs):
        """
        Update station attributes.

        :param station_id: Station primary key
        :param kwargs: Fields to update (station_name, files_path)
        :return: Tuple (success: bool, result: Station or error message)
        """
        try:
            with Session(engine) as session:
                # Check if station exists
                station = session.query(Station).filter_by(station_id=station_id).first()

                if not station:
                    return False, f"Station not found: {station_id}"

                # If updating name, check it doesn't exist for another station
                if "station_name" in kwargs:
                    new_name = kwargs["station_name"]
                    exists = session.query(Station).filter_by(station_name=new_name).first()

                    if exists and exists.station_id != station_id:
                        return False, f"Station name already exists: {new_name}"

                # Update fields
                for key, value in kwargs.items():
                    if hasattr(station, key):
                        setattr(station, key, value)

                session.commit()
                session.refresh(station)

                return True, station

        except Exception as e:
            self.__logger.error(f"Error updating station: {e}")
            return False, "Error updating station"
