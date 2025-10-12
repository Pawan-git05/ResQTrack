from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models import Admin, NGO, Volunteer
from ..utils import verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/login")
def login():
	data = request.get_json(silent=True) or {}
	email = (data.get("email") or "").strip().lower()
	password = data.get("password") or ""
	role = (data.get("role") or "").upper()

	if not email or not password or role not in {"ADMIN", "NGO", "VOLUNTEER"}:
		return {"error": "email, password and role are required"}, 400

	user = None
	identity = {"role": role}
	if role == "ADMIN":
		user = Admin.query.filter_by(email=email).first()
	elif role == "NGO":
		user = NGO.query.filter_by(email=email).first()
	elif role == "VOLUNTEER":
		user = Volunteer.query.filter_by(email=email).first()

	if not user or not verify_password(password, getattr(user, "password_hash", "")):
		return {"error": "invalid credentials"}, 401

	identity.update({"id": user.id, "email": email})
	token = create_access_token(identity=identity)
	return {"access_token": token}, 200
