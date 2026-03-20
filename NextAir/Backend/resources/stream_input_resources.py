"""
StreamInput resource endpoints.

REST API resources for stream input management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from flask.views import MethodView
from models import StreamInputModel
from controller import admin_required
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from schemas import StreamInputSchema, StreamInputUpdateSchema

blp = Blueprint("StreamInputs", __name__, description="Stream input management operations")


@blp.route("/stream-inputs")
class StreamInputCollection(MethodView):
    """
    Resource for stream input collection operations.
    """

    @blp.response(200, StreamInputSchema(many=True))
    @jwt_required()
    def get(self):
        """
        Get all stream inputs.

        :return: List of all stream inputs
        """
        return StreamInputModel.get_all()

    @blp.arguments(StreamInputSchema)
    @blp.response(201, StreamInputSchema)
    @admin_required
    def post(self, stream_input_data):
        """
        Create a new stream input.

        :param stream_input_data: Stream input data from request body
        :return: Created stream input
        """
        # Validate name uniqueness
        if StreamInputModel.find_by_name(stream_input_data["name"]):
            abort(400, message="A stream input with that name already exists.")

        # Validate url uniqueness
        if StreamInputModel.find_by_url(stream_input_data["url"]):
            abort(400, message="A stream input with that URL already exists.")

        stream_input = StreamInputModel(
            name=stream_input_data["name"],
            url=stream_input_data["url"],
            channel=stream_input_data["channel"],
            sample_rate=stream_input_data["sample_rate"],
            block_size=stream_input_data["block_size"]
        )
        stream_input.save_to_db()

        return stream_input


@blp.route("/stream-inputs/<int:stream_input_id>")
class StreamInputItem(MethodView):
    """
    Resource for individual stream input operations.
    """

    @blp.response(200, StreamInputSchema)
    @jwt_required()
    def get(self, stream_input_id):
        """
        Get a stream input by ID.

        :param stream_input_id: Stream input ID
        :return: Stream input data
        """
        stream_input = StreamInputModel.find_by_id(stream_input_id)
        if not stream_input:
            abort(404, message="Stream input not found.")
        return stream_input

    @blp.arguments(StreamInputUpdateSchema)
    @blp.response(200, StreamInputSchema)
    @admin_required
    def patch(self, stream_input_data, stream_input_id):
        """
        Update a stream input partially.

        :param stream_input_data: Updated stream input data from request body
        :param stream_input_id: Stream input ID
        :return: Updated stream input data
        """
        stream_input = StreamInputModel.find_by_id(stream_input_id)
        if not stream_input:
            abort(404, message="Stream input not found.")

        # Validate name uniqueness if updating
        if "name" in stream_input_data:
            existing = StreamInputModel.find_by_name(stream_input_data["name"])
            if existing and existing.stream_input_id != stream_input_id:
                abort(400, message="A stream input with that name already exists.")
            stream_input.name = stream_input_data["name"]

        # Validate url uniqueness if updating
        if "url" in stream_input_data:
            existing = StreamInputModel.find_by_url(stream_input_data["url"])
            if existing and existing.stream_input_id != stream_input_id:
                abort(400, message="A stream input with that URL already exists.")
            stream_input.url = stream_input_data["url"]

        if "channel" in stream_input_data:
            stream_input.channel = stream_input_data["channel"]
        if "sample_rate" in stream_input_data:
            stream_input.sample_rate = stream_input_data["sample_rate"]
        if "block_size" in stream_input_data:
            stream_input.block_size = stream_input_data["block_size"]

        stream_input.save_to_db()
        return stream_input

    @blp.response(204)
    @admin_required
    def delete(self, stream_input_id):
        """
        Delete a stream input by ID.

        :param stream_input_id: Stream input ID
        :return: None
        """
        stream_input = StreamInputModel.find_by_id(stream_input_id)
        if not stream_input:
            abort(404, message="Stream input not found.")
        stream_input.delete_from_db()
