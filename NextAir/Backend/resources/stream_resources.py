"""
Stream resource endpoints.

REST API resources for stream management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from flask.views import MethodView
from controller import admin_required
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from models import StreamModel, StationModel
from schemas import StreamSchema, StreamUpdateSchema, PlainStreamSchema

blp = Blueprint("Streams", __name__, description="Stream management operations")


@blp.route("/streams")
class StreamCollection(MethodView):
    """
    Resource for stream collection operations.
    """

    @blp.response(200, PlainStreamSchema(many=True))
    @jwt_required()
    def get(self):
        """
        Get all streams.

        :return: List of all streams
        """
        return StreamModel.get_all()

    @blp.arguments(StreamSchema)
    @blp.response(201, StreamSchema)
    @admin_required
    def post(self, stream_data):
        """
        Create a new stream.

        :param stream_data: Stream data from request body
        :return: Created stream
        """
        station = StationModel.find_by_id(stream_data["station_id"])
        if not station:
            abort(404, message="Station not found.")

        if StreamModel.find_by_name(stream_data["stream_name"]):
            abort(400, message="A stream with that name already exists.")

        if StreamModel.find_by_external_id(stream_data["external_id"]):
            abort(400, message="A stream with that external ID already exists.")

        stream = StreamModel(
            station_id=stream_data["station_id"],
            stream_name=stream_data["stream_name"],
            external_id=stream_data["external_id"]
        )
        stream.save_to_db()

        return stream


@blp.route("/streams/<int:stream_id>")
class StreamItem(MethodView):
    """
    Resource for individual stream operations.
    """

    @blp.response(200, StreamSchema)
    @jwt_required()
    def get(self, stream_id):
        """
        Get a stream by ID.

        :param stream_id: Stream ID
        :return: Stream data
        """
        stream = StreamModel.find_by_id(stream_id)
        if not stream:
            abort(404, message="Stream not found.")
        return stream

    @blp.arguments(StreamUpdateSchema)
    @blp.response(200, StreamSchema)
    @admin_required
    def patch(self, stream_data, stream_id):
        """
        Update a stream partially.

        :param stream_data: Updated stream data from request body
        :param stream_id: Stream ID
        :return: Updated stream data
        """
        stream = StreamModel.find_by_id(stream_id)
        if not stream:
            abort(404, message="Stream not found.")

        # Validate station_id if updating
        if "station_id" in stream_data:
            if not StationModel.find_by_id(stream_data["station_id"]):
                abort(404, message="Station not found.")
            stream.station_id = stream_data["station_id"]

        # Validate stream_name uniqueness if updating
        if "stream_name" in stream_data:
            existing = StreamModel.find_by_name(stream_data["stream_name"])
            if existing and existing.stream_id != stream_id:
                abort(400, message="A stream with that name already exists.")
            stream.stream_name = stream_data["stream_name"]

        # Validate external_id uniqueness if updating
        if "external_id" in stream_data:
            existing = StreamModel.find_by_external_id(stream_data["external_id"])
            if existing and existing.stream_id != stream_id:
                abort(400, message="A stream with that external ID already exists.")
            stream.external_id = stream_data["external_id"]

        stream.save_to_db()
        return stream

    @blp.response(204)
    @admin_required
    def delete(self, stream_id):
        """
        Delete a stream by ID.

        :param stream_id: Stream ID
        :return: None
        """
        stream = StreamModel.find_by_id(stream_id)
        if not stream:
            abort(404, message="Stream not found.")
        stream.delete_from_db()
