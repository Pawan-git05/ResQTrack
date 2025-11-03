from flask import Blueprint, request
from ..extensions import db, limiter
from ..models import NGO, Volunteer
from ..utils import hash_password

registrations_bp = Blueprint("registrations", __name__, url_prefix="/register")


@registrations_bp.post("/ngo")
@limiter.limit("10 per hour")
def register_ngo():
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	email = (data.get("email") or "").strip().lower()
	phone = (data.get("phone") or "").strip()
	password = data.get("password") or ""
	if not name or not email or not phone or not password:
		return {"error": "name, email, phone, and password required"}, 400

	# Prevent duplicate email errors
	if NGO.query.filter_by(email=email).first():
		return {"error": "email already registered"}, 409

	ngo = NGO(
		name=name,
		email=email,
		password_hash=hash_password(password),
		phone=phone,
		location=data.get("location"),
		operating_zones=data.get("operating_zones"),
	)
	db.session.add(ngo)
	db.session.commit()
	return {"message": "NGO registration submitted", "ngo_id": ngo.id}, 201


@registrations_bp.post("/volunteer")
@limiter.limit("10 per hour")
def register_volunteer():
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	email = (data.get("email") or "").strip().lower()
	phone = (data.get("phone") or "").strip()
	password = data.get("password") or ""
	if not name or not email or not phone or not password:
		return {"error": "name, email, phone, and password required"}, 400

	if Volunteer.query.filter_by(email=email).first():
		return {"error": "email already registered"}, 409

	vol = Volunteer(
		name=name,
		email=email,
		password_hash=hash_password(password),
		phone=phone,
		location=data.get("location"),
		expertise=data.get("expertise"),
		availability=data.get("availability"),
	)
	db.session.add(vol)
	db.session.commit()
	return {"message": "Volunteer registration submitted", "volunteer_id": vol.id}, 201
