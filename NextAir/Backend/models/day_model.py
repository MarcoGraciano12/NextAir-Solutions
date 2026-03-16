"""
Day model definition.

Defines the DayModel class representing days of the week (lookup table).
This is a static table with 7 fixed records.

Author: Marco Graciano
Date: 2026-03-13
"""

from db import db


class DayModel(db.Model):
    """
    Day of week model (lookup table).
    """

    __tablename__ = "day"

    day_id = db.Column(db.Integer, primary_key=True)
    day_name = db.Column(db.String(20), unique=True, nullable=False)

    # Relationship: 1 day → N blocks (no cascade, static table)
    blocks = db.relationship('BlockModel', backref='day', lazy=True)

    @classmethod
    def find_by_id(cls, day_id):
        """
        Find a day by ID.

        :param day_id: The day ID to search for (1-7)
        :return: DayModel instance if found, None otherwise
        """
        return cls.query.filter_by(day_id=day_id).first()

    @classmethod
    def find_by_name(cls, day_name):
        """
        Find a day by name.

        :param day_name: The day name to search for
        :return: DayModel instance if found, None otherwise
        """
        return cls.query.filter_by(day_name=day_name).first()

    @classmethod
    def get_all(cls):
        """
        Get all days.

        :return: List of all DayModel instances (7 days)
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Save the current day instance to the database.
        Note: Used only for initial population.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert day instance to dictionary.

        :return: Dictionary with day attributes
        """
        return {
            'day_id': self.day_id,
            'day_name': self.day_name,
            'blocks_count': len(self.blocks)
        }
