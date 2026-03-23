"""
Stream resource endpoints.

REST API resources for stream management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from controller import admin_required, controller
from schemas import StreamSchema, StreamUpdateSchema, PlainStreamSchema

blp = Blueprint("Streams", __name__, description="Stream management operations")


@blp.route("/streams")
class StreamCollection(MethodView):
    """
    Resource for stream collection operations.
    """

    @blp.response(200, PlainStreamSchema(many=True))
    # @jwt_required()
    def get(self):
        """
        Get all streams.

        :return: List of all streams
        """
        streams, error = controller.get_all_streams()

        if error:
            abort(500, message=error)

        return streams

    @blp.arguments(StreamSchema)
    @blp.response(201, StreamSchema)
    # @admin_required
    def post(self, stream_data):
        """
        Create a new stream.

        :param stream_data: Stream data from request body
        :return: Created stream
        """
        stream, error = controller.create_stream(**stream_data)

        if error:
            abort(400, message=error)

        return stream


@blp.route("/streams/<string:stream_name>")
class StreamItem(MethodView):
    """
    Resource for individual stream operations.
    """

    @blp.response(200, StreamSchema)
    # @jwt_required()
    def get(self, stream_name):
        """
        Get a stream by ID.

        :param stream_name: Stream Name
        :return: Stream data
        """
        stream, error = controller.get_stream(stream_name=stream_name)

        if error:
            abort(404, message=error)

        return stream

    # @blp.arguments(StreamUpdateSchema)
    # @blp.response(200, StreamSchema)
    # @admin_required
    # def patch(self, stream_data, stream_id):
    #     """
    #     Update a stream partially.
    #
    #     :param stream_data: Updated stream data from request body
    #     :param stream_id: Stream ID
    #     :return: Updated stream data
    #     """
    #     stream = StreamModel.find_by_id(stream_id)
    #     if not stream:
    #         abort(404, message="Stream not found.")
    #
    #     # Validate station_id if updating
    #     if "station_id" in stream_data:
    #         if not StationModel.find_by_id(stream_data["station_id"]):
    #             abort(404, message="Station not found.")
    #         stream.station_id = stream_data["station_id"]
    #
    #     # Validate stream_name uniqueness if updating
    #     if "stream_name" in stream_data:
    #         existing = StreamModel.find_by_name(stream_data["stream_name"])
    #         if existing and existing.stream_id != stream_id:
    #             abort(400, message="A stream with that name already exists.")
    #         stream.stream_name = stream_data["stream_name"]
    #
    #     # Validate external_id uniqueness if updating
    #     if "external_id" in stream_data:
    #         existing = StreamModel.find_by_external_id(stream_data["external_id"])
    #         if existing and existing.stream_id != stream_id:
    #             abort(400, message="A stream with that external ID already exists.")
    #         stream.external_id = stream_data["external_id"]
    #
    #     stream.save_to_db()
    #     return stream

    @blp.response(204)
    # @admin_required
    def delete(self, stream_name):
        """
        Delete a stream by ID.

        :param stream_name: Stream Name
        :return: None
        """
        stream, error = controller.delete_stream(stream_name=stream_name)

        if error:
            abort(404, message=error)


@blp.route("/stations/<string:station_name>/streams")
class StationStreamCollection(MethodView):
    """
    Resource for station-specific stream operations.
    """

    @blp.response(200, StreamSchema(many=True))
    # @jwt_required()
    def get(self, station_name):
        """
        Get all streams for a station.

        :param station_name: Station name
        :return: List of streams for the station
        """
        streams, error = controller.get_streams_for_station(station_name=station_name)

        if error:
            abort(404, message=error)

        return streams