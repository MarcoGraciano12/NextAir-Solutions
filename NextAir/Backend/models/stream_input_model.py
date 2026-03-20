"""
StreamInput model definition.

Defines the StreamInputModel class representing audio input sources
with configuration parameters. Includes helper methods for database
operations and stream input lookups.

Author: Marco Graciano
Date: 2026-03-13
"""

from db import db


class StreamInputModel(db.Model):
    """
    Audio input source model.
    """

    __tablename__ = "stream_input"

    stream_input_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    channel = db.Column(db.Integer, nullable=False)
    sample_rate = db.Column(db.Integer, nullable=False)
    block_size = db.Column(db.Integer, nullable=False)

    @classmethod
    def find_by_id(cls, stream_input_id):
        """
        Find a stream input by ID.

        :param stream_input_id: The stream input ID to search for
        :return: StreamInputModel instance if found, None otherwise
        """
        return cls.query.filter_by(stream_input_id=stream_input_id).first()

    @classmethod
    def find_by_name(cls, name):
        """
        Find a stream input by name.

        :param name: The stream input name to search for
        :return: StreamInputModel instance if found, None otherwise
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_url(cls, url):
        """
        Find a stream input by URL.

        :param url: The stream input URL to search for
        :return: StreamInputModel instance if found, None otherwise
        """
        return cls.query.filter_by(url=url).first()

    @classmethod
    def get_all(cls):
        """
        Get all stream inputs.

        :return: List of all StreamInputModel instances
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Save the current stream input instance to the database.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current stream input instance from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert stream input instance to dictionary.

        :return: Dictionary with stream input attributes
        """
        return {
            'stream_input_id': self.stream_input_id,
            'name': self.name,
            'url': self.url,
            'channel': self.channel,
            'sample_rate': self.sample_rate,
            'block_size': self.block_size
        }
