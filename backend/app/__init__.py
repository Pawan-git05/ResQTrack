from flask import Flask, request
import os
from backend.config import Config
from .extensions import db, migrate, cors, mail
from .extensions import init_limiter
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
from backend.logging_config import configure_logging


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Uploads
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Remove JWT completely
    # jwt.init_app(app)  # ❌ REMOVED

    # CORS Fix (Full Open)
    cors.init_app(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Handle OPTIONS (important for CSV upload)
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return ("", 200)

    mail.init_app(app)

    # Rate limiter
    init_limiter(app)

    # Import models
    from . import models  # noqa

    # Register blueprints under "/api"
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(cases_bp, url_prefix="/api")
    app.register_blueprint(registrations_bp, url_prefix="/api")
    app.register_blueprint(hospitals_bp, url_prefix="/api")
    app.register_blueprint(donations_bp, url_prefix="/api")
    app.register_blueprint(uploads_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(data_bp, url_prefix="/api")

    # Logging
    configure_logging(app)

    # HTTP error handler
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        return {"error": e.name, "message": e.description}, e.code

    # Catch-all errors
    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        logging.exception("Unhandled exception")
        return {"error": "Internal Server Error"}, 500

    return app
