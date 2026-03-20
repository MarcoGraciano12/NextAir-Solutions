"""
API Controller for streaming system management.

Author: Marco Graciano
Date: March 20, 2026

Description: Main controller for managing radio stations and audio streaming operations.
"""

from .station import Station
from logging import Logger, getLogger
from models import StationModel, stream_input_model

class APIController:

    def __init__(self, logger: Logger = None):
        self.__stations = {}
        self.__stream_inputs = {}
        self.__logger = logger or getLogger(self.__class__.__name__)

    def start_streaming(self, station_name: str, stream_name: str) -> dict:
        """
        Start streaming for station stream.

        :param station_name: Station name
        :param stream_name: Stream name
        :return: Dict with status and message
        """
        station = self.__stations.get(station_name)

        if station:
            return station.start(stream_name)

        station_model = StationModel.find_by_name(station_name)

        if not station_model:
            self.__logger.warning(f"Station '{station_name}' not found in database")
            return {'status': False, 'message': f"Station '{station_name}' not found"}

        station = Station(**station_model.to_dict())
        self.__logger.info(f"Station loaded: {station}")
        result = station.start(stream_name)

        if not result['status']:
            self.__logger.error(f"Failed to start streaming for '{station_name}/{stream_name}': {result['message']}")
            return result

        self.__stations[station_name] = station
        self.__logger.info(f"Streaming started for '{station_name}/{stream_name}'")
        return result

    def stop_streaming(self, station_name: str, stream_name: str) -> dict:
        """
        Stop streaming for station stream.

        :param station_name: Station name
        :param stream_name: Stream name
        :return: Dict with status and message
        """
        station = self.__stations.get(station_name)

        if not station:
            self.__logger.warning(f"Station '{station_name}' not found in memory")
            return {'status': False, 'message': f"Station '{station_name}' not active"}

        result = station.stop(stream_name)
        self.__logger.info(f"Streaming stopped for '{station_name}/{stream_name}'")
        return result

    def restart_streaming(self, station_name: str, stream_name: str) -> dict:
        """
        Restart streaming for station stream.

        :param station_name: Station name
        :param stream_name: Stream name
        :return: Dict with status and message
        """
        self.stop_streaming(station_name, stream_name)
        return self.start_streaming(station_name, stream_name)

    def reload_streaming(self, station_name: str, stream_name: str) -> dict:
        """
        Reload streaming configuration for station stream.

        :param station_name: Station name
        :param stream_name: Stream name
        :return: Dict with status and message
        """
        station = self.__stations.get(station_name)

        if not station:
            self.__logger.warning(f"Station '{station_name}' not found in memory")
            return {'status': False, 'message': f"Station '{station_name}' not active"}

        result = station.reload(stream_name)
        self.__logger.info(f"Streaming reloaded for '{station_name}/{stream_name}'")
        return result
