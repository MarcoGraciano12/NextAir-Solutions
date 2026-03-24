"""
Schemas for serialization and validation.

Marshmallow schemas for station, stream, day, and block data validation,
serialization, and deserialization. Uses Plain schemas to avoid circular references.

Author: Marco Graciano
Date: 2026-03-13
"""

from marshmallow import Schema, fields


# Plain schemas (without relationships)

class PlainStationSchema(Schema):
    """
    Plain station schema without relationships.
    """
    station_id = fields.Int(dump_only=True)
    station_name = fields.Str(required=True)
    files_path = fields.Str(required=True)


class PlainStreamSchema(Schema):
    """
    Plain stream schema without relationships.
    """
    stream_id = fields.Int(dump_only=True)
    station_id = fields.Int(required=True)
    stream_name = fields.Str(required=True)
    external_id = fields.Int(required=True)


class PlainDaySchema(Schema):
    """
    Plain day schema without relationships.
    """
    day_id = fields.Int(dump_only=True)
    day_name = fields.Str(required=True)


class PlainBlockSchema(Schema):
    """
    Plain block schema without relationships.
    """
    block_id = fields.Int(dump_only=True)
    stream_id = fields.Int(required=True)
    day_id = fields.Int(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    source_name = fields.Str(required=True)
    schedule_name = fields.Str(required=True)


# Full schemas (with relationships)

class StationSchema(PlainStationSchema):
    """
    Station schema with nested streams.
    """
    streams = fields.List(fields.Nested(PlainStreamSchema()), dump_only=True)
    streams_count = fields.Int(dump_only=True)


class StreamSchema(PlainStreamSchema):
    """
    Stream schema with nested relationships.
    """
    station = fields.Nested(PlainStationSchema(), dump_only=True)
    blocks = fields.List(fields.Nested(PlainBlockSchema()), dump_only=True)
    blocks_count = fields.Int(dump_only=True)


class StreamCreateSchema(Schema):
    """
    Schema for stream creation with station_name.
    """
    station_name = fields.Str(required=True)
    stream_name = fields.Str(required=True)
    external_id = fields.Int(required=True)


class DaySchema(PlainDaySchema):
    """
    Day schema with nested blocks.
    """
    blocks = fields.List(fields.Nested(PlainBlockSchema()), dump_only=True)
    blocks_count = fields.Int(dump_only=True)


class BlockSchema(PlainBlockSchema):
    """
    Block schema with nested relationships.
    """
    stream = fields.Nested(PlainStreamSchema(), dump_only=True)
    day = fields.Nested(PlainDaySchema(), dump_only=True)


# Update schemas

class StationUpdateSchema(Schema):
    """
    Schema for partial station updates.
    """
    station_name = fields.Str()
    files_path = fields.Str()


class StreamUpdateSchema(Schema):
    """
    Schema for partial stream updates.
    """
    station_id = fields.Int()
    stream_name = fields.Str()
    external_id = fields.Int()


class BlockUpdateSchema(Schema):
    """
    Schema for partial block updates.
    """
    stream_id = fields.Int()
    day_id = fields.Int()
    start_time = fields.Time()
    end_time = fields.Time()
    source_name = fields.Str()
    schedule_name = fields.Str()


# Transmission Resources

class Transmission(Schema):
    station_name = fields.Str(required=True)
    stream_name = fields.Str(required=True)