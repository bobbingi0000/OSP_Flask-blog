"""Models module — Defines database models for the Y2K blog.

Uses Flask-SQLAlchemy to define the blog's data schema.
Currently provides the GuestbookEntry model; a Post model
is planned for future releases.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db: SQLAlchemy = SQLAlchemy()
"""SQLAlchemy database instance."""


class GuestbookEntry(db.Model):
    """Model representing a Y2K mini-homepage guestbook entry.

    Stores guestbook data in a Cyworld-style format.
    Each entry contains an author, content, and creation timestamp.

    Attributes:
        id (int): Unique identifier (Primary Key, Auto Increment).
        author (str): Name of the guestbook author. Max 50 characters,
            required field.
        content (str): Guestbook message content. Max 500 characters,
            required field.
        created_at (datetime): Timestamp of creation.
            Defaults to ``datetime.utcnow``.

    Example:
        >>> entry = GuestbookEntry(author="Neo", content="Follow the white rabbit")
        >>> db.session.add(entry)
        >>> db.session.commit()
    """

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Returns a debug-friendly string representation of the model.

        Returns:
            str: A string in ``<GuestbookEntry author>`` format.
        """
        return f'<GuestbookEntry {self.author}>'
