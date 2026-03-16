"""
Station model definition.

Defines the StationModel class representing radio stations in the system.
Includes helper methods for database operations and station lookups.

Author: Marco Graciano
Date: 2026-03-13
"""

from db import db


class StationModel(db.Model):
    """
    Radio station model.
    """

    __tablename__ = "stations"

    station_id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(255), nullable=False)
    files_path = db.Column(db.String(500), nullable=False)

    # Relationship: 1 station → N streams
    streams = db.relationship('StreamModel', backref='station', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def find_by_id(cls, station_id):
        """
        Find a station by ID.

        :param station_id: The station ID to search for
        :return: StationModel instance if found, None otherwise
        """
        return cls.query.filter_by(station_id=station_id).first()

    @classmethod
    def find_by_name(cls, station_name):
        """
        Find a station by name.

        :param station_name: The station name to search for
        :return: StationModel instance if found, None otherwise
        """
        return cls.query.filter_by(station_name=station_name).first()

    @classmethod
    def get_all(cls):
        """
        Get all stations.

        :return: List of all StationModel instances
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Save the current station instance to the database.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current station instance from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert station instance to dictionary.

        :return: Dictionary with station attributes
        """
        return {
            'station_id': self.station_id,
            'station_name': self.station_name,
            'files_path': self.files_path,
            'streams_count': len(self.streams)
        }