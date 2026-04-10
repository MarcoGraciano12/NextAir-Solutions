
from db import engine
from models import Sources, Playlist
from logging import getLogger
import datetime
from sqlalchemy.orm import Session
from typing import List, Tuple, Type, Any
from .sql_connection import get_sources


__logger = getLogger("Schedules")


# ======================================================================================================================
# SOURCE
# ======================================================================================================================
def add_sources(stream_id: int, weekday: int, items: List[Tuple]):
    """
    Bulk insert sources for a stream.

    :param stream_id: Stream ID
    :param weekday: Day of week (0=Monday, 6=Sunday)
    :param items: List of tuples (start_time, end_time, source)
    :return: List of created Sources objects, None on error
    """
    with Session(engine) as session:
        sources = [
            Sources(
                stream_id=stream_id,
                start_time=start_time,
                end_time=end_time,
                source=source,
                weekday=weekday
            )
            for start_time, end_time, source in items
        ]
        session.bulk_save_objects(sources)
        session.commit()
        return sources


def remove_sources(stream_id: int, weekday: int):
    """
    Delete sources for specific stream and weekday.

    :param stream_id: Stream ID
    :param weekday: Day of week (0=Monday, 6=Sunday)
    :return: True if success, False otherwise
    """
    with Session(engine) as session:
        session.query(Sources).filter_by(stream_id=stream_id, weekday=weekday).delete()
        session.commit()


def update_sources(external_id: int, stream_id: int, weekday: int, date: datetime):
    """
    Update sources for stream by fetching and replacing data.

    :param external_id: Station external ID
    :param stream_id: Stream ID
    :param weekday: Day of week (0=Monday, 6=Sunday)
    :param date: Date to query
    :return: List of created Sources objects, None on error
    """
    try:
        data = get_sources(external_id=external_id, date=date)

        if not data:
            __logger.warning(f"No sources found for external_id {external_id}")
            return None

        remove_sources(stream_id, weekday)

        return add_sources(stream_id, weekday, data)

    except Exception as error:
        __logger.error(f"Failed to update sources: {error}")
        return None


def get_weekday_sources(stream_id: int, weekday: int):
    """
    Get all sources for specific stream and weekday.

    :param stream_id: Stream ID
    :param weekday: Day of week (0=Monday, 6=Sunday)
    :return: List of Sources objects, None on error
    """
    try:
        with Session(engine) as session:
            return session.query(Sources).filter_by(
                stream_id=stream_id,
                weekday=weekday
            ).order_by(Sources.start_time).all()

    except Exception as error:
        __logger.error(f"Failed to get sources for stream {stream_id}, weekday {weekday}: {error}")
        return None


# ======================================================================================================================
# PLAYLIST
# ======================================================================================================================
def get_schedule_block(stream_id: int, broadcast_day: datetime.datetime, hour: int):
    """
    Get playlist blocks for specific stream, day and hour.

    :param stream_id: Stream ID
    :param broadcast_day: Broadcast datetime
    :param hour: Hour to filter (0-23)
    :return: List of Playlist objects, None on error
    """
    try:
        filters = [
            Playlist.stream_id == stream_id,
            Playlist.broadcast_day == broadcast_day.date(),
            Playlist.start_time >= datetime.time(hour, 0, 0)
        ]

        if hour < 23:
            filters.append(Playlist.start_time < datetime.time(hour + 1, 0, 0))

        with Session(engine) as session:
            return session.query(Playlist).filter(*filters).order_by(Playlist.start_time).all()

    except Exception as error:
        __logger.error(f"Failed to get playlist blocks: {error}")
        return None


def add_schedule_block(stream_id: int, broadcast_day: datetime.datetime, items: List[Tuple]):
    """
    Bulk insert playlist blocks for a stream.

    :param stream_id: Stream ID
    :param broadcast_day: Broadcast date
    :param items: List of tuples (type_code, start_time, end_time, item_code, source, spot_id)
    :return: List of created Playlist objects
    """
    with Session(engine) as session:
        playlist = [
            Playlist(
                stream_id=stream_id,
                type_code=type_code,
                start_time=start_time,
                end_time=end_time,
                item_code=item_code,
                source=source,
                spot_id=spot_id,
                broadcast_day=broadcast_day.date()
            )
            for type_code, start_time, end_time, item_code, source, spot_id, _ in items
        ]

        session.bulk_save_objects(playlist)
        session.commit()
        return playlist


def remove_schedule_block(stream_id: int, broadcast_day: datetime.datetime, hour: int):
    """
    Delete playlist blocks for specific hour.

    :param stream_id: Stream ID
    :param broadcast_day: Broadcast date
    :param hour: Hour to filter (0-23)
    """
    filters = [
        Playlist.stream_id == stream_id,
        Playlist.broadcast_day == broadcast_day.date(),
        Playlist.start_time >= datetime.time(hour, 0, 0)
    ]

    if hour < 23:
        filters.append(Playlist.start_time < datetime.time(hour + 1, 0, 0))

    with Session(engine) as session:
        session.query(Playlist).filter(*filters).delete()
        session.commit()
