"""
SQL Server connection pool and query execution.

Author: Marco
Date: 2025-03-26
"""

import os
from datetime import datetime
from logging import getLogger
from typing import List, Tuple
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


def get_station_sources(external_id: int, date: datetime = None) -> List[Tuple] | None:
    """
    Get station sources from SQL Server function.

    :param external_id: Station external ID
    :param date: Date to query
    :return: List of tuples with source data, False on error
    """
    try:
        date = date or datetime.now()

        query = text("""
            SELECT DISTINCT DayOfWeek, StartTime, EndTime, SourceCode
            FROM dbo.fn_GetStationSources(:date, :external_id)
            ORDER BY DayOfWeek, StartTime
        """)

        with __engine.connect() as conn:
            result = conn.execute(query, {"date": date, "external_id": external_id})
            return result.fetchall()

    except Exception as e:
        __logger.error(f"Error fetching station sources: {e}")
        return None


def get_station_playlist(external_id: int, date: datetime = None) -> List[Tuple] | None:
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


if __name__ == "__main__":
    # now = datetime(2026, 3, 27, 0, 26, 55)
    data = get_station_playlist(20)

    for item in data:
        print(item)
