"""
Database initialization utilities.

Handles initial population of static lookup tables with fixed data.
Run after db.create_all() to populate required reference data.

Author: Marco Graciano
Date: 2026-03-13
"""

from db import db
from models import DayModel
from logging import getLogger


logger = getLogger(__name__)


def init_days(app):
    """
    Populate day table with weekdays in correct order.

    Creates 7 day records with fixed IDs (1-7) corresponding to
    weekday positions (1=Monday, 7=Sunday). Skips if data already exists.

    :param app: Flask application instance
    :return: None
    """
    with app.app_context():
        # Check if days already exist
        if DayModel.query.count() > 0:
            logger.info("Days table already initialized")
            return

        # Create days with fixed IDs
        days = [
            DayModel(day_id=1, day_name='Lunes'),
            DayModel(day_id=2, day_name='Martes'),
            DayModel(day_id=3, day_name='Miércoles'),
            DayModel(day_id=4, day_name='Jueves'),
            DayModel(day_id=5, day_name='Viernes'),
            DayModel(day_id=6, day_name='Sábado'),
            DayModel(day_id=7, day_name='Domingo')
        ]

        # Add all days to session
        for day in days:
            db.session.add(day)

        # Commit transaction
        db.session.commit()
        logger.info("Days table initialized successfully with 7 records")


def init_database(app):
    """
    Initialize all static lookup tables.

    Master function that calls all table initialization functions.
    Call this after db.create_all() in app.py.

    :param app: Flask application instance
    :return: None
    """
    init_days(app)
