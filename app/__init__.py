"""Y2K-themed Flask blog application package.

Main application module for Cyber Y2K Personal Digital Space.
Creates the Flask app instance, initializes the database,
and provides Swagger UI API documentation via Flasgger.
"""

from flask import Flask
from flasgger import Swagger
from app.config import Config
from app.models import db, GuestbookEntry  # noqa: F401
from app.routes import register_routes


def create_app(config_class: type = Config) -> Flask:
    """Flask application factory function.

    Creates a Flask app instance, initializes extensions, and
    registers URL routes. A custom configuration class can be
    injected for testing purposes.

    Args:
        config_class (type): Flask configuration class.
            Defaults to Config.

    Returns:
        Flask: A fully initialized Flask application instance.
            Swagger UI, SQLAlchemy, and routes are all registered.
    """
    application = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static',
    )
    application.config.from_object(config_class)

    # ── Flasgger (Swagger UI) Configuration ─────────────────────
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    swagger_template = {
        "info": {
            "title": "🛸 Cyber Y2K Blog API",
            "description": (
                "A personal blog web service API with early-2000s Y2K aesthetics.\n\n"
                "Built on Cyworld mini-homepage & chrome texture themes,\n"
                "providing Home, Write, and Guestbook features."
            ),
            "version": "1.0.0",
            "contact": {
                "name": "Y2K Blog Developer",
                "url": "https://github.com/bobbingi0000/OSP_Flask-blog",
            },
            "license": {"name": "MIT"},
        },
        "basePath": "/",
        "schemes": ["http"],
        "tags": [
            {"name": "Home", "description": "Main landing page (blog front door)"},
            {"name": "Write", "description": "Terminal-style writing page"},
            {"name": "Guestbook", "description": "Y2K mini-homepage guestbook"},
        ],
    }

    # ── Initialize Extensions ───────────────────────────────────
    db.init_app(application)
    Swagger(application, config=swagger_config, template=swagger_template)
    register_routes(application)

    with application.app_context():
        db.create_all()

    return application
