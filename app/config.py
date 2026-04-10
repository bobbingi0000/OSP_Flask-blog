"""Configuration module — Defines settings for the Y2K blog Flask app.

Manages the configuration class used across the Flask application,
including SQLAlchemy database URI and tracking options.
"""

import os

basedir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
"""Absolute path to the project root directory."""


class Config:
    """Default configuration class for the Flask application.

    Determines the behavior of Flask and SQLAlchemy through
    environment variables or default values. This class can be
    subclassed and overridden for testing.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): SQLite database file path.
            Defaults to ``app.db`` in the project root.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disables the
            SQLAlchemy event system modification tracking.
            Defaults to False.
    """

    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
