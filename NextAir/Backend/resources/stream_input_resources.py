"""
StreamInput resource endpoints.

REST API resources for stream input management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from controller import admin_required, controller
from schemas import StreamInputSchema, StreamInputUpdateSchema

blp = Blueprint("StreamInputs", __name__, description="Stream input management operations")


@blp.route("/stream-inputs")
class StreamInputCollection(MethodView):
    """
    Resource for stream input collection operations.
    """

    @blp.response(200, StreamInputSchema(many=True))
    # @jwt_required()
    def get(self):
        """
        Get all stream inputs.

        :return: List of all stream inputs
        """
        inputs, error = controller.retrieve_all_stream_inputs()

        if error:
            abort(500, message=error)

        return inputs

    @blp.arguments(StreamInputSchema)
    @blp.response(201, StreamInputSchema)
    # @admin_required
    def post(self, stream_input_data):
        """
        Create a new stream input.

        :param stream_input_data: Stream input data from request body
        :return: Created stream input
        """
        stream_input, error = controller.create_stream_input(**stream_input_data)

        if error:
            abort(400, message=error)

        return stream_input


@blp.route("/stream-inputs/<int:stream_input_id>")
class StreamInputItem(MethodView):
    """
    Resource for individual stream input operations.
    """

    @blp.response(200, StreamInputSchema)
    # @jwt_required()
    def get(self, stream_input_id):
        """
        Get a stream input by ID.

        :param stream_input_id: Stream input ID
        :return: Stream input data
        """
        stream_input, error = controller.retrieve_stream_input(stream_input_id=stream_input_id)

        if error:
            abort(404, message=error)

        return stream_input

    # @blp.arguments(StreamInputUpdateSchema)
    # @blp.response(200, StreamInputSchema)
    # @admin_required
    # def patch(self, stream_input_data, stream_input_id):
    #     """
    #     Update a stream input partially.
    #
    #     :param stream_input_data: Updated stream input data from request body
    #     :param stream_input_id: Stream input ID
    #     :return: Updated stream input data
    #     """
    #     stream_input = StreamInputModel.find_by_id(stream_input_id)
    #     if not stream_input:
    #         abort(404, message="Stream input not found.")
    #
    #     # Validate name uniqueness if updating
    #     if "name" in stream_input_data:
    #         existing = StreamInputModel.find_by_name(stream_input_data["name"])
    #         if existing and existing.stream_input_id != stream_input_id:
    #             abort(400, message="A stream input with that name already exists.")
    #         stream_input.name = stream_input_data["name"]
    #
    #     # Validate url uniqueness if updating
    #     if "url" in stream_input_data:
    #         existing = StreamInputModel.find_by_url(stream_input_data["url"])
    #         if existing and existing.stream_input_id != stream_input_id:
    #             abort(400, message="A stream input with that URL already exists.")
    #         stream_input.url = stream_input_data["url"]
    #
    #     if "channel" in stream_input_data:
    #         stream_input.channel = stream_input_data["channel"]
    #     if "sample_rate" in stream_input_data:
    #         stream_input.sample_rate = stream_input_data["sample_rate"]
    #     if "block_size" in stream_input_data:
    #         stream_input.block_size = stream_input_data["block_size"]
    #
    #     stream_input.save_to_db()
    #     return stream_input
    #
    @blp.response(204)
    # @admin_required
    def delete(self, stream_input_id):
        """
        Delete a stream input by ID.

        :param stream_input_id: Stream input ID
        :return: None
        """
        stream_input, error = controller.delete_stream_input(stream_input_id=stream_input_id)

        if error:
            abort(404, message=error)


@blp.route("/stream-inputs-status")
class StreamInputStatusCollection(MethodView):
    """
    Resource for stream input status operations.
    """

    @blp.response(200)
    # @jwt_required()
    def get(self):
        """
        Get status of all stream inputs.

        :return: List of stream input statuses
        """
        statuses, error = controller.get_stream_inputs_status()

        if error:
            abort(500, message=error)

        return statuses