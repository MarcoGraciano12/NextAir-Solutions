"""
Streaming management resources for Flask API.

Author: Marco Graciano
Date: March 20, 2026

Description: REST endpoints for streaming control operations.
"""

from flask.views import MethodView
from controller import APIController
from flask_smorest import Blueprint, abort


blp = Blueprint("Streaming", __name__, description="Streaming management operations")
controller = APIController()


@blp.route("/streaming/start/<string:station_name>/<string:stream_name>")
class StartStreaming(MethodView):

    @blp.response(200)
    def post(self, station_name, stream_name):
        """
        Start stream transmission.
        """
        result = controller.start_streaming(station_name, stream_name)

        if not result['status']:
            abort(400, message=result['message'])

        return result


@blp.route("/streaming/stop/<string:station_name>/<string:stream_name>")
class StopStreaming(MethodView):

    @blp.response(200)
    def post(self, station_name, stream_name):
        """
        Stop stream transmission.
        """
        result = controller.stop_streaming(station_name, stream_name)

        if not result['status']:
            abort(400, message=result['message'])

        return result


@blp.route("/streaming/restart/<string:station_name>/<string:stream_name>")
class RestartStreaming(MethodView):

    @blp.response(200)
    def post(self, station_name, stream_name):
        """
        Restart stream transmission.
        """
        result = controller.restart_streaming(station_name, stream_name)

        if not result['status']:
            abort(400, message=result['message'])

        return result


@blp.route("/streaming/reload/<string:station_name>/<string:stream_name>")
class ReloadStreaming(MethodView):

    @blp.response(200)
    def post(self, station_name, stream_name):
        """
        Reload stream configuration.
        """
        result = controller.reload_streaming(station_name, stream_name)

        if not result['status']:
            abort(400, message=result['message'])

        return result