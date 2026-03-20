"""
Broadcast model definition.

Defines the BroadcastModel class representing broadcast destinations
for audio streams. Includes helper methods for database operations
and broadcast lookups.

Author: Marco Graciano
Date: 2026-03-13
"""

from db import db


class BroadcastModel(db.Model):
    """
    Broadcast destination model.
    """

    __tablename__ = "broadcast"

    broadcast_id = db.Column(db.Integer, primary_key=True)
    stream_id = db.Column(db.Integer, db.ForeignKey('streams.stream_id'), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    user = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    channels = db.Column(db.Integer, nullable=False)
    sample_rate = db.Column(db.Integer, nullable=False)
    block_size = db.Column(db.Integer, nullable=False)
    bitrate = db.Column(db.String(50), nullable=False)

    @classmethod
    def find_by_id(cls, broadcast_id):
        """
        Find a broadcast by ID.

        :param broadcast_id: The broadcast ID to search for
        :return: BroadcastModel instance if found, None otherwise
        """
        return cls.query.filter_by(broadcast_id=broadcast_id).first()

    @classmethod
    def find_by_name(cls, name):
        """
        Find a broadcast by name.

        :param name: The broadcast name to search for
        :return: BroadcastModel instance if found, None otherwise
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_url(cls, url):
        """
        Find a broadcast by URL.

        :param url: The broadcast URL to search for
        :return: BroadcastModel instance if found, None otherwise
        """
        return cls.query.filter_by(url=url).first()

    @classmethod
    def find_by_stream_id(cls, stream_id):
        """
        Find all broadcasts for a stream.

        :param stream_id: The stream ID to search for
        :return: List of BroadcastModel instances
        """
        return cls.query.filter_by(stream_id=stream_id).all()

    @classmethod
    def get_all(cls):
        """
        Get all broadcasts.

        :return: List of all BroadcastModel instances
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Save the current broadcast instance to the database.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current broadcast instance from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert broadcast instance to dictionary.
        Excludes password for security.

        :return: Dictionary with broadcast attributes
        """
        return {
            'broadcast_id': self.broadcast_id,
            'stream_id': self.stream_id,
            'name': self.name,
            'url': self.url,
            'user': self.user,
            'channels': self.channels,
            'sample_rate': self.sample_rate,
            'block_size': self.block_size,
            'bitrate': self.bitrate
        }
