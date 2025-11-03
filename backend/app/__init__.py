from flask import Flask
import os
from ..config import Config
from .extensions import db, migrate, jwt, cors, mail, limiter
from .routes.health import health_bp
from .routes.auth import auth_bp
from .routes.cases import cases_bp
from .routes.registrations import registrations_bp
from .routes.hospitals import hospitals_bp
from .routes.donations import donations_bp
from .routes.uploads import uploads_bp
from .routes.admin import admin_bp
from .routes.data import data_bp
from werkzeug.exceptions import HTTPException
import logging
from ..logging_config import configure_logging


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure uploads directory exists
    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # Restrict CORS using configured origins with credentials support
    cors.init_app(app, resources={
        r"/*": {
            "origins": app.config.get("CORS_ORIGINS", "*"),
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    mail.init_app(app)
    limiter.init_app(app)

    # Import models so that migrations can discover them
    from . import models  # noqa: F401

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(donations_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(data_bp)

    # Configure logging
    configure_logging(app)

    # Global error handlers returning JSON
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        response = {"error": e.name, "message": e.description}
        return response, e.code

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        logging.exception("Unhandled exception")
        return {"error": "Internal Server Error"}, 500

    return app
