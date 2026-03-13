"""
Token blocklist model definition.

Defines the TokenBlocklistModel class for storing revoked JWT tokens.
Includes automatic cleanup methods for expired tokens.

Author: Marco Graciano
Date: February 09, 2026
"""

from db import db


class BlocklistModel(db.Model):
    """
    Model for storing revoked JWT tokens.
    """

    __tablename__ = "token_blocklist"

    jti = db.Column(db.String(255), primary_key=True)
    expires_at = db.Column(db.DateTime, nullable=False)

    @classmethod
    def is_jti_blocklisted(cls, jti):
        """
        Check if a token JTI is blocklisted.

        :param jti: The JWT ID to check
        :return: True if blocklisted, False otherwise
        """
        return cls.query.filter_by(jti=jti).first() is not None

    def save_to_db(self):
        """
        Save the current token to the blocklist.

        :return: None
        """
        db.session.add(self)
        db.session.commit()
