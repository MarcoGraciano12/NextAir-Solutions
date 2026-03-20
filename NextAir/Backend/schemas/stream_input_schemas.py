"""
StreamInput schemas for serialization and validation.

Marshmallow schemas for stream input data validation, serialization,
and deserialization. Includes schemas for stream input CRUD operations
and partial updates.

Author: Marco Graciano
Date: 2026-03-13
"""

from marshmallow import Schema, fields


class PlainStreamInputSchema(Schema):
    """
    Plain stream input schema without relationships.
    """
    stream_input_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)
    channel = fields.Int(required=True)
    sample_rate = fields.Int(required=True)
    block_size = fields.Int(required=True)


class StreamInputSchema(PlainStreamInputSchema):
    """
    Stream input schema with nested relationships.
    """
    pass  # No additional relationships for now


class StreamInputUpdateSchema(Schema):
    """
    Schema for partial stream input updates.
    """
    name = fields.Str()
    url = fields.Str()
    channel = fields.Int()
    sample_rate = fields.Int()
    block_size = fields.Int()
