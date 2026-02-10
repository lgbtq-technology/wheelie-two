import logging
import os

from flask import Flask

from app.config import config


def create_app(config_name=None):
    """
    Main application factory.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Register blueprints
    from app.routes import register_blueprints

    register_blueprints(app)

    return app
