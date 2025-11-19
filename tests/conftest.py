import os
import pytest
from backend.app import create_app
from backend.app.extensions import db


@pytest.fixture()
def app(tmp_path, monkeypatch):
	# Use MySQL connector URL (from test environment)
	monkeypatch.setenv("DATABASE_URL", "mysql+mysqlconnector://root:1234@localhost/resqtrack")
	monkeypatch.setenv("ALLOWED_ORIGINS", "*")
	monkeypatch.setenv("UPLOAD_FOLDER", str(tmp_path / "uploads"))
	app = create_app()
	with app.app_context():
		db.create_all()
		yield app
		db.session.remove()
		db.drop_all()


@pytest.fixture()
def client(app):
	return app.test_client()
