"""
Block resource endpoints.

REST API resources for block management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from flask.views import MethodView
from controller import admin_required
from flask_smorest import Blueprint, abort
from schemas import BlockSchema, BlockUpdateSchema
from models import BlockModel, StreamModel, DayModel


blp = Blueprint("Blocks", __name__, description="Block management operations")


@blp.route("/blocks")
class BlockCollection(MethodView):
    """
    Resource for block collection operations.
    """

    @blp.response(200, BlockSchema(many=True))
    def get(self):
        """
        Get all blocks.

        :return: List of all blocks
        """
        return BlockModel.get_all()

    @blp.arguments(BlockSchema)
    @blp.response(201, BlockSchema)
    @admin_required
    def post(self, block_data):
        """
        Create a new block.

        :param block_data: Block data from request body
        :return: Created block
        """
        # Validate stream exists
        if not StreamModel.find_by_id(block_data["stream_id"]):
            abort(404, message="Stream not found.")

        # Validate day exists
        if not DayModel.find_by_id(block_data["day_id"]):
            abort(404, message="Day not found.")

        block = BlockModel(
            stream_id=block_data["stream_id"],
            day_id=block_data["day_id"],
            start_time=block_data["start_time"],
            end_time=block_data["end_time"],
            source_name=block_data["source_name"],
            schedule_name=block_data["schedule_name"]
        )
        block.save_to_db()

        return block


@blp.route("/blocks/<int:block_id>")
class BlockItem(MethodView):
    """
    Resource for individual block operations.
    """

    @blp.response(200, BlockSchema)
    def get(self, block_id):
        """
        Get a block by ID.

        :param block_id: Block ID
        :return: Block data
        """
        block = BlockModel.find_by_id(block_id)
        if not block:
            abort(404, message="Block not found.")
        return block

    @blp.arguments(BlockUpdateSchema)
    @blp.response(200, BlockSchema)
    @admin_required
    def patch(self, block_data, block_id):
        """
        Update a block partially.

        :param block_data: Updated block data from request body
        :param block_id: Block ID
        :return: Updated block data
        """
        block = BlockModel.find_by_id(block_id)
        if not block:
            abort(404, message="Block not found.")

        if "stream_id" in block_data:
            if not StreamModel.find_by_id(block_data["stream_id"]):
                abort(404, message="Stream not found.")
            block.stream_id = block_data["stream_id"]

        if "day_id" in block_data:
            if not DayModel.find_by_id(block_data["day_id"]):
                abort(404, message="Day not found.")
            block.day_id = block_data["day_id"]

        if "start_time" in block_data:
            block.start_time = block_data["start_time"]
        if "end_time" in block_data:
            block.end_time = block_data["end_time"]
        if "source_name" in block_data:
            block.source_name = block_data["source_name"]
        if "schedule_name" in block_data:
            block.schedule_name = block_data["schedule_name"]

        block.save_to_db()
        return block

    @blp.response(204)
    @admin_required
    def delete(self, block_id):
        """
        Delete a block by ID.

        :param block_id: Block ID
        :return: None
        """
        block = BlockModel.find_by_id(block_id)
        if not block:
            abort(404, message="Block not found.")
        block.delete_from_db()


@blp.route("/streams/<int:stream_id>/days/<int:day_id>/blocks")
class StreamDayBlocks(MethodView):
    """
    Resource for getting blocks by stream and day.
    """

    @blp.response(200, BlockSchema(many=True))
    def get(self, stream_id, day_id):
        """
        Get all blocks for a specific stream and day.

        :param stream_id: Stream ID
        :param day_id: Day ID
        :return: List of blocks ordered by start time
        """
        blocks = BlockModel.find_by_stream_and_day(stream_id, day_id)
        return blocks
