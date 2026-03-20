"""
Broadcast resource endpoints.

REST API resources for broadcast management including CRUD operations.

Author: Marco Graciano
Date: 2026-03-13
"""

from flask.views import MethodView
from controller import admin_required
from passlib.hash import pbkdf2_sha256
from flask_smorest import Blueprint, abort
from models import BroadcastModel, StreamModel
from schemas import BroadcastSchema, BroadcastUpdateSchema

blp = Blueprint("Broadcasts", __name__, description="Broadcast management operations")


@blp.route("/broadcasts")
class BroadcastCollection(MethodView):
    """
    Resource for broadcast collection operations.
    """

    @blp.response(200, BroadcastSchema(many=True))
    def get(self):
        """
        Get all broadcasts.

        :return: List of all broadcasts
        """
        return BroadcastModel.get_all()

    @blp.arguments(BroadcastSchema)
    @blp.response(201, BroadcastSchema)
    @admin_required
    def post(self, broadcast_data):
        """
        Create a new broadcast.

        :param broadcast_data: Broadcast data from request body
        :return: Created broadcast
        """
        # Validate stream exists
        stream = StreamModel.find_by_id(broadcast_data["stream_id"])
        if not stream:
            abort(404, message="Stream not found.")

        # Validate name uniqueness
        if BroadcastModel.find_by_name(broadcast_data["name"]):
            abort(400, message="A broadcast with that name already exists.")

        # Validate url uniqueness
        if BroadcastModel.find_by_url(broadcast_data["url"]):
            abort(400, message="A broadcast with that URL already exists.")

        broadcast = BroadcastModel(
            stream_id=broadcast_data["stream_id"],
            name=broadcast_data["name"],
            url=broadcast_data["url"],
            user=broadcast_data["user"],
            password=pbkdf2_sha256.hash(broadcast_data["password"]),
            channels=broadcast_data["channels"],
            sample_rate=broadcast_data["sample_rate"],
            block_size=broadcast_data["block_size"],
            bitrate=broadcast_data["bitrate"]
        )
        broadcast.save_to_db()

        return broadcast


@blp.route("/broadcasts/<int:broadcast_id>")
class BroadcastItem(MethodView):
    """
    Resource for individual broadcast operations.
    """

    @blp.response(200, BroadcastSchema)
    def get(self, broadcast_id):
        """
        Get a broadcast by ID.

        :param broadcast_id: Broadcast ID
        :return: Broadcast data
        """
        broadcast = BroadcastModel.find_by_id(broadcast_id)
        if not broadcast:
            abort(404, message="Broadcast not found.")
        return broadcast

    @blp.arguments(BroadcastUpdateSchema)
    @blp.response(200, BroadcastSchema)
    @admin_required
    def patch(self, broadcast_data, broadcast_id):
        """
        Update a broadcast partially.

        :param broadcast_data: Updated broadcast data from request body
        :param broadcast_id: Broadcast ID
        :return: Updated broadcast data
        """
        broadcast = BroadcastModel.find_by_id(broadcast_id)
        if not broadcast:
            abort(404, message="Broadcast not found.")

        # Validate stream_id if updating
        if "stream_id" in broadcast_data:
            stream = StreamModel.find_by_id(broadcast_data["stream_id"])
            if not stream:
                abort(404, message="Stream not found.")
            broadcast.stream_id = broadcast_data["stream_id"]

        # Validate name uniqueness if updating
        if "name" in broadcast_data:
            existing = BroadcastModel.find_by_name(broadcast_data["name"])
            if existing and existing.broadcast_id != broadcast_id:
                abort(400, message="A broadcast with that name already exists.")
            broadcast.name = broadcast_data["name"]

        # Validate url uniqueness if updating
        if "url" in broadcast_data:
            existing = BroadcastModel.find_by_url(broadcast_data["url"])
            if existing and existing.broadcast_id != broadcast_id:
                abort(400, message="A broadcast with that URL already exists.")
            broadcast.url = broadcast_data["url"]

        # Hash password if updating
        if "password" in broadcast_data:
            broadcast.password = pbkdf2_sha256.hash(broadcast_data["password"])

        if "user" in broadcast_data:
            broadcast.user = broadcast_data["user"]
        if "channels" in broadcast_data:
            broadcast.channels = broadcast_data["channels"]
        if "sample_rate" in broadcast_data:
            broadcast.sample_rate = broadcast_data["sample_rate"]
        if "block_size" in broadcast_data:
            broadcast.block_size = broadcast_data["block_size"]
        if "bitrate" in broadcast_data:
            broadcast.bitrate = broadcast_data["bitrate"]

        broadcast.save_to_db()
        return broadcast

    @blp.response(204)
    @admin_required
    def delete(self, broadcast_id):
        """
        Delete a broadcast by ID.

        :param broadcast_id: Broadcast ID
        :return: None
        """
        broadcast = BroadcastModel.find_by_id(broadcast_id)
        if not broadcast:
            abort(404, message="Broadcast not found.")
        broadcast.delete_from_db()
