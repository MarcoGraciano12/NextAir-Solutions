"""
Broadcast schemas for serialization and validation.

Marshmallow schemas for broadcast data validation, serialization,
and deserialization. Includes schemas for broadcast CRUD operations
and partial updates.

Author: Marco Graciano
Date: 2026-03-13
"""

from marshmallow import Schema, fields
from .plain_schemas import PlainStreamSchema

class PlainBroadcastSchema(Schema):
    """
    Plain broadcast schema without relationships.
    """
    broadcast_id = fields.Int(dump_only=True)
    stream_id = fields.Int(required=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)
    user = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    channels = fields.Int(required=True)
    sample_rate = fields.Int(required=True)
    block_size = fields.Int(required=True)
    bitrate = fields.Str(required=True)


class BroadcastSchema(PlainBroadcastSchema):
    """
    Broadcast schema with nested relationships.
    """
    stream = fields.Nested(PlainStreamSchema(), dump_only=True)


class BroadcastUpdateSchema(Schema):
    """
    Schema for partial broadcast updates.
    """
    stream_id = fields.Int()
    name = fields.Str()
    url = fields.Str()
    user = fields.Str()
    password = fields.Str(load_only=True)
    channels = fields.Int()
    sample_rate = fields.Int()
    block_size = fields.Int()
    bitrate = fields.Str()
