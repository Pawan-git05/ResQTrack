from flask import Blueprint, request
from ..extensions import db, limiter
from ..models import Admin, NGO, Volunteer
from ..utils import verify_password

auth_bp = Blueprint("auth", "auth", url_prefix="/auth")

@auth_bp.post("/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = (data.get("role") or "").upper()

    if not email or not password or role not in {"ADMIN", "NGO", "VOLUNTEER"}:
        return {"error": "email, password and role are required"}, 400

    if role == "ADMIN":
        user = Admin.query.filter_by(email=email).first()
    elif role == "NGO":
        user = NGO.query.filter_by(email=email).first()
    else:
        user = Volunteer.query.filter_by(email=email).first()

    if not user or not verify_password(password, getattr(user, "password_hash", "")):
        return {"error": "invalid credentials"}, 401

    return {
        "message": "login successful (JWT disabled)",
        "role": role,
        "id": user.id
    }, 200
