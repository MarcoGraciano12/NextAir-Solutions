"""
Station resource endpoints.

REST API resources for station management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from controller import admin_required, controller
from schemas import StationSchema, StationUpdateSchema

blp = Blueprint("Stations", __name__, description="Station management operations")


@blp.route("/stations")
class StationCollection(MethodView):
    """
    Resource for station collection operations.
    """

    @blp.response(200, StationSchema(many=True))
    # @jwt_required()
    def get(self):
        """
        Get all stations.

        :return: List of all stations
        """
        stations, error = controller.retrieve_all_stations()

        if error:
            abort(500, message=error)

        return stations

    @blp.arguments(StationSchema)
    @blp.response(201, StationSchema)
    # @admin_required
    def post(self, station_data):
        """
        Create a new station.

        :param station_data: Station data from request body
        :return: Created station
        """
        station, error = controller.create_station(**station_data)

        if error:
            abort(400, message=error)

        return station


@blp.route("/stations/<int:station_id>")
class StationItem(MethodView):
    """
    Resource for individual station operations.
    """

    @blp.response(200, StationSchema)
    # @jwt_required()
    def get(self, station_id):
        """
        Get a station by ID.

        :param station_id: Station ID
        :return: Station data
        """
        station, error = controller.retrieve_station(station_id=station_id)

        if error:
            abort(404, message=error)

        return station

    # @blp.arguments(StationUpdateSchema)
    # @blp.response(200, StationSchema)
    # # @admin_required
    # def patch(self, station_data, station_id):
    #     """
    #     Update a station partially.
    #
    #     :param station_data: Updated station data from request body
    #     :param station_id: Station ID
    #     :return: Updated station data
    #     """
    #     station = StationModel.find_by_id(station_id)
    #     if not station:
    #         abort(404, message="Station not found.")
    #
    #     # Save original name before modification
    #     original_name = station.station_name
    #
    #     if "station_name" in station_data:
    #         existing = StationModel.find_by_name(station_data['station_name'])
    #         if existing and existing.station_id != station_id:
    #             abort(400, message="A station with that name already exists.")
    #         station.station_name = station_data["station_name"]
    #
    #     if "files_path" in station_data:
    #         station.files_path = station_data["files_path"]
    #
    #     # Use original name to find in dict
    #     if not controller.update_station(station_name=original_name, **station_data):
    #         abort(500, message="Failed to update station in controller.")
    #
    #     station.save_to_db()
    #     return station

    @blp.response(204)
    # @admin_required
    def delete(self, station_id):
        """
        Delete a station by ID.

        :param station_id: Station ID
        :return: None
        """
        station, error = controller.delete_station(station_id=station_id)

        if error:
            abort(404, message=error)
