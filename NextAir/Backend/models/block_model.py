"""
Block model definition.

Defines the BlockModel class representing schedule blocks for audio streams.
Each block belongs to a stream and a day, with start/end times and source info.

Author: Marco Graciano
Date: 2026-03-13
"""

from db import db


class BlockModel(db.Model):
    """
    Schedule block model.
    """

    __tablename__ = "block"

    block_id = db.Column(db.Integer, primary_key=True)
    stream_id = db.Column(db.Integer, db.ForeignKey('streams.stream_id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.day_id'), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    source_name = db.Column(db.String(255), nullable=False)
    schedule_name = db.Column(db.String(255), nullable=False)

    @classmethod
    def find_by_id(cls, block_id):
        """
        Find a block by ID.

        :param block_id: The block ID to search for
        :return: BlockModel instance if found, None otherwise
        """
        return cls.query.filter_by(block_id=block_id).first()

    @classmethod
    def find_by_stream_id(cls, stream_id):
        """
        Find all blocks for a stream.

        :param stream_id: The stream ID to search for
        :return: List of BlockModel instances
        """
        return cls.query.filter_by(stream_id=stream_id).order_by(cls.day_id, cls.start_time).all()

    @classmethod
    def find_by_day_id(cls, day_id):
        """
        Find all blocks for a specific day.

        :param day_id: The day ID to search for
        :return: List of BlockModel instances
        """
        return cls.query.filter_by(day_id=day_id).order_by(cls.start_time).all()

    @classmethod
    def find_by_stream_and_day(cls, stream_id, day_id):
        """
        Find all blocks for a specific stream and day.

        :param stream_id: The stream ID to search for
        :param day_id: The day ID to search for
        :return: List of BlockModel instances ordered by start time
        """
        return cls.query.filter_by(stream_id=stream_id, day_id=day_id).order_by(cls.start_time).all()

    @classmethod
    def get_all(cls):
        """
        Get all blocks.

        :return: List of all BlockModel instances
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Save the current block instance to the database.

        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current block instance from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Convert block instance to dictionary.

        :return: Dictionary with block attributes
        """
        return {
            'block_id': self.block_id,
            'stream_id': self.stream_id,
            'day_id': self.day_id,
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'source_name': self.source_name,
            'schedule_name': self.schedule_name
        }
