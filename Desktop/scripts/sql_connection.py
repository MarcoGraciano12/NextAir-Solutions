"""
SQL Server connection pool and query execution.

Author: Marco
Date: 2025-03-26
"""

import os
from datetime import datetime
from logging import getLogger
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Logger
__logger = getLogger(__name__)

# Build connection string
__conn_str = (
    f"mssql+pyodbc://{os.getenv('SQL_USER')}:{os.getenv('SQL_PASSWORD')}"
    f"@{os.getenv('SQL_SERVER')}:{os.getenv('SQL_PORT')}/{os.getenv('SQL_NAME')}"
    f"?driver={os.getenv('SQL_DRIVER')}"
)

# Create engine with connection pool
__engine = create_engine(
    __conn_str,
    pool_size=20,  # Permanent connections in pool
    max_overflow=30,  # Additional connections if needed (max total = 50)
    pool_pre_ping=True,  # Verify connection before use
    pool_recycle=3600  # Recycle connections after 1 hour
)

__logger.info("SQL Server connection pool initialized")


def get_sources(external_id: int, date: datetime = None):
    """
    Get station sources from SQL Server function.

    :param external_id: Station external ID
    :param date: Date to query
    :return: List of tuples with source data, False on error
    """
    try:
        date = date or datetime.now()

        query = text("""
            SELECT DISTINCT StartTime, EndTime, SourceCode
            FROM dbo.fn_GetStationSources(:date, :external_id)
            ORDER BY StartTime
        """)

        with __engine.connect() as conn:
            result = conn.execute(query, {"date": date, "external_id": external_id})
            return result.fetchall()

    except Exception as e:
        __logger.error(f"Error fetching station sources: {e}")
        return None


def get_playlist(external_id: int, date: datetime = None):
    """
    Get station playlist from SQL Server function.

    :param external_id: Station external ID
    :param date: Date to query
    :return: List of tuples with playlist data, False on error
    """
    try:
        date = date or datetime.now()

        query = text("""
           SELECT DISTINCT ItemType, StartTime, EndTime, ItemCode, Source, SpotId, SequenceInCut
           FROM dbo.fn_GetStationPlaylist(:date, :external_id)
           ORDER BY StartTime, SequenceInCut
        """)

        with __engine.connect() as conn:
            result = conn.execute(query, {"date": date, "external_id": external_id})
            return result.fetchall()

    except Exception as e:
        __logger.error(f"Error fetching station playlist: {e}")
        return None


def get_playlist_block(external_id: int, date: datetime = None, hour: int = None):
    """
    Get station playlist filtered by specific hour.

    :param external_id: Station external ID
    :param date: Date to query
    :param hour: Hour to filter (0-23)
    :return: List of tuples with playlist data, None on error
    """
    try:
        date = date or datetime.now()
        hour = hour if hour is not None else datetime.now().hour

        hour_start = f"{hour:02d}:00:00"

        # Build WHERE clause conditionally
        if hour < 23:
            hour_end = f"{hour + 1:02d}:00:00"
            where_clause = "WHERE StartTime >= CAST(:hour_start AS TIME) AND StartTime < CAST(:hour_end AS TIME)"
            params = {"date": date, "external_id": external_id, "hour_start": hour_start, "hour_end": hour_end}
        else:
            where_clause = "WHERE StartTime >= CAST(:hour_start AS TIME)"
            params = {"date": date, "external_id": external_id, "hour_start": hour_start}

        query = text(f"""
           SELECT DISTINCT ItemType, StartTime, EndTime, ItemCode, Source, SpotId, SequenceInCut
           FROM dbo.fn_GetStationPlaylist(:date, :external_id)
           {where_clause}
           ORDER BY StartTime, SequenceInCut
        """)

        with __engine.connect() as conn:
            result = conn.execute(query, params)
            return result.fetchall()

    except Exception as e:
        __logger.error(f"Error fetching station playlist block: {e}")
        return None
