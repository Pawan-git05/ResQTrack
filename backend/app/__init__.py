from flask import Flask
import os
from ..config import Config
from .extensions import db, migrate, jwt, cors, mail
from .routes.health import health_bp
from .routes.auth import auth_bp
from .routes.cases import cases_bp
from .routes.registrations import registrations_bp
from .routes.hospitals import hospitals_bp
from .routes.donations import donations_bp
from .routes.uploads import uploads_bp
from .routes.admin import admin_bp


def create_app(config_class: type = Config) -> Flask:
	app = Flask(__name__)
	app.config.from_object(config_class)

	# Ensure uploads directory exists
	os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)
	jwt.init_app(app)
	cors.init_app(app)
	mail.init_app(app)

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

	return app
