"""
Stream model definition.

Defines the StreamModel class representing audio streams in the system.
Includes helper methods for database operations and stream lookups.

Author: Marco Graciano
Date: 2026-03-13
"""
from enum import unique

from db import db


class StreamModel(db.Model):
    """
    Audio stream model.
    """

    __tablename__ = "streams"

    stream_id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    stream_name = db.Column(db.String(255), unique=True, nullable=False)
    external_id = db.Column(db.Integer, unique=True, nullable=False)

    # Relationship: 1 stream → N blocks
    blocks = db.relationship('BlockModel', backref='stream', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def find_by_id(cls, stream_id):
        """
        Find a stream by ID.

        :param stream_id: The stream ID to search for
        :return: StreamModel instance if found, None otherwise
        """
        return cls.query.filter_by(stream_id=stream_id).first()

    @classmethod
    def find_by_name(cls, stream_name):
        """
        Find a stream by name.

        :param stream_name: The stream name to search for
        :return: StreamModel instance if found, None otherwise
        """
        return cls.query.filter_by(stream_name=stream_name).first()

    @classmethod
    def find_by_external_id(cls, external_id):
        """
        Find a stream by external ID.

        :param external_id: The external ID to search for
        :return: StreamModel instance if found, None otherwise
        """
        return cls.query.filter_by(external_id=external_id).first()

    @classmethod
    def find_by_station_id(cls, station_id):
        """
        Find all streams for a station.

        :param station_id: The station ID to search for
        :return: List of StreamModel instances
        """
        return cls.query.filter_by(station_id=station_id).all()

    @classmethod
    def get_all(cls):
        """
        Get all streams.

        :return: List of all StreamModel instances
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Save the current stream instance to the database.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current stream instance from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert stream instance to dictionary.

        :return: Dictionary with stream attributes
        """
        return {
            'stream_id': self.stream_id,
            'station_id': self.station_id,
            'stream_name': self.stream_name,
            'external_id': self.external_id,
            'blocks_count': len(self.blocks)
        }
