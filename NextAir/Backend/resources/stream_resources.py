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
from schemas import StreamSchema, StreamUpdateSchema, PlainStreamSchema, StreamCreateSchema, Transmission

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

    @blp.arguments(StreamCreateSchema)
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
        Get a stream by name.

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
        Delete a stream by name.

        :param stream_name: Stream Name
        :return: None
        """
        stream, error = controller.delete_stream(stream_name=stream_name)

        if error:
            abort(404, message=error)


# ==================================================================================================================
# SINGLE TRANSMISSION
# ==================================================================================================================

@blp.route("/streams/start/<string:station_name>/<string:stream_name>")
class StartTransmission(MethodView):
    """
    Start audio stream transmission.
    """

    @blp.response(204)
    # @jwt_required()
    def post(self, station_name, stream_name):
        """
        Start streaming for specified station and stream.

        :param station_name: Station identifier
        :param stream_name: Stream identifier
        :return: Operation status
        """
        status, error, = controller.start_transmission(station_name=station_name, stream_name=stream_name)

        if error:
            abort(400, message=error)


@blp.route("/streams/stop/<string:station_name>/<string:stream_name>")
class StopTransmission(MethodView):
    """
    Stop audio stream transmission.
    """

    @blp.response(204)
    # @jwt_required()
    def post(self, station_name, stream_name):
        """
        Stop streaming for specified station and stream.

        :param station_name: Station identifier
        :param stream_name: Stream identifier
        :return: Operation status
        """
        status, error, = controller.stop_transmission(station_name=station_name, stream_name=stream_name)

        if error:
            abort(400, message=error)


@blp.route("/streams/restart/<string:station_name>/<string:stream_name>")
class RestartTransmission(MethodView):
    """
    Restart audio stream transmission.
    """

    @blp.response(204)
    # @jwt_required()
    def post(self, station_name, stream_name):
        """
        Restart streaming for specified station and stream.

        :param station_name: Station identifier
        :param stream_name: Stream identifier
        :return: Operation status
        """
        # TODO: Get stream instance, call stop() then start()

        return {"station_name": station_name, "stream_name": stream_name}


@blp.route("/streams/reload/<string:station_name>/<string:stream_name>")
class ReloadTransmission(MethodView):
    """
    Reload audio stream configuration.
    """

    @blp.response(204)
    # @jwt_required()
    def post(self, station_name, stream_name):
        """
        Reload configuration for specified station and stream.

        :param station_name: Station identifier
        :param stream_name: Stream identifier
        :return: Operation status
        """
        # TODO: Get stream instance, reload config, restart if running

        return {"station_name": station_name, "stream_name": stream_name}


# ==================================================================================================================
# STATION TRANSMISSIONS
# ==================================================================================================================


@blp.route("/streams/start/<string:station_name>")
class StartStationTransmission(MethodView):
    """
    Start all streams for a station.
    """

    @blp.response(204)
    # @jwt_required()
    def post(self, station_name):
        """
        Start all stream transmissions for specified station.

        :param station_name: name of the station
        :return: Operation status
        """
        status, error = controller.start_station_transmissions(station_name=station_name)

        if error:
            abort(400, message=error)


@blp.route("/streams/stop/<string:station_name>")
class StopStationTransmission(MethodView):
    """
    Stop all streams for a station.
    """

    @blp.response(204)
    # @jwt_required()
    def post(self, station_name):
        """
        Stop all stream transmissions for specified station.

        :param station_name: name of the station
        :return: Operation status
        """
        status, error = controller.stop_station_transmissions(station_name=station_name)

        if error:
            abort(400, message=error)


@blp.route("/streams/restart/<string:station_name>")
class RestartStationTransmission(MethodView):
    """
    Restart all streams for a station.
    """

    @blp.response(200)
    # @jwt_required()
    def post(self, data):
        """
        Restart all stream transmissions for specified station.

        :param data: Request data with station_name
        :return: Operation status
        """
        station_name = data.get("station_name")
        # TODO: Get all streams for station, stop and start them

        return {"station_name": station_name, "status": "restarted"}


@blp.route("/streams/reload/<string:station_name>")
class ReloadStationTransmission(MethodView):
    """
    Reload configuration for all streams in a station.
    """

    @blp.response(200)
    # @jwt_required()
    def post(self, data):
        """
        Reload configuration for all streams in specified station.

        :param data: Request data with station_name
        :return: Operation status
        """
        station_name = data.get("station_name")
        # TODO: Get all streams for station, reload config

        return {"station_name": station_name, "status": "reloaded"}


# ==================================================================================================================
# ALL TRANSMISSIONS
# ==================================================================================================================


@blp.route("/streams/start")
class StartAllTransmissions(MethodView):
    """
    Start all station transmissions.
    """

    @blp.response(200)
    # @jwt_required()
    def post(self):
        """
        Start all stream transmissions for all stations.

        :return: Operation status
        """
        # TODO: Get all stations and start all streams

        return {"status": "all_started"}


@blp.route("/streams/stop")
class StopAllTransmissions(MethodView):
    """
    Stop all station transmissions.
    """

    @blp.response(200)
    # @jwt_required()
    def post(self):
        """
        Stop all stream transmissions for all stations.

        :return: Operation status
        """
        # TODO: Get all stations and stop all streams

        return {"status": "all_stopped"}


@blp.route("/streams/restart")
class RestartAllTransmissions(MethodView):
    """
    Restart all station transmissions.
    """

    @blp.response(200)
    # @jwt_required()
    def post(self):
        """
        Restart all stream transmissions for all stations.

        :return: Operation status
        """
        # TODO: Get all stations, stop and start all streams

        return {"status": "all_restarted"}


@blp.route("/streams/reload")
class ReloadAllTransmissions(MethodView):
    """
    Reload configuration for all transmissions.
    """

    @blp.response(200)
    # @jwt_required()
    def post(self):
        """
        Reload configuration for all streams in all stations.

        :return: Operation status
        """
        # TODO: Get all stations, reload config for all streams

        return {"status": "all_reloaded"}
