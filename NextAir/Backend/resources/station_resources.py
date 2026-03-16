"""
Station resource endpoints.

REST API resources for station management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from models import StationModel
from flask.views import MethodView
from controller import admin_required
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from schemas import StationSchema, StationUpdateSchema

blp = Blueprint("Stations", __name__, description="Station management operations")


@blp.route("/stations")
class StationCollection(MethodView):
    """
    Resource for station collection operations.
    """

    @blp.response(200, StationSchema(many=True))
    @jwt_required()
    def get(self):
        """
        Get all stations.

        :return: List of all stations
        """
        return StationModel.get_all()

    @blp.arguments(StationSchema)
    @blp.response(201, StationSchema)
    @admin_required
    def post(self, station_data):
        """
        Create a new station.

        :param station_data: Station data from request body
        :return: Created station
        """
        if StationModel.find_by_name(station_data["station_name"]):
            abort(400, message="A station with that name already exists.")

        station = StationModel(
            station_name=station_data["station_name"],
            files_path=station_data["files_path"]
        )
        station.save_to_db()

        return station


@blp.route("/stations/<int:station_id>")
class StationItem(MethodView):
    """
    Resource for individual station operations.
    """

    @blp.response(200, StationSchema)
    @jwt_required()
    def get(self, station_id):
        """
        Get a station by ID.

        :param station_id: Station ID
        :return: Station data
        """
        station = StationModel.find_by_id(station_id)
        if not station:
            abort(404, message="Station not found.")
        return station

    @blp.arguments(StationUpdateSchema)
    @blp.response(200, StationSchema)
    @admin_required
    def patch(self, station_data, station_id):
        """
        Update a station partially.

        :param station_data: Updated station data from request body
        :param station_id: Station ID
        :return: Updated station data
        """
        station = StationModel.find_by_id(station_id)
        if not station:
            abort(404, message="Station not found.")

        if "station_name" in station_data:
            station.station_name = station_data["station_name"]
        if "files_path" in station_data:
            station.files_path = station_data["files_path"]

        station.save_to_db()
        return station

    @blp.response(204)
    @admin_required
    def delete(self, station_id):
        """
        Delete a station by ID.

        :param station_id: Station ID
        :return: None
        """
        station = StationModel.find_by_id(station_id)
        if not station:
            abort(404, message="Station not found.")
        station.delete_from_db()
