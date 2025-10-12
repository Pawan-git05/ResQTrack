from flask import Blueprint, request
from ..extensions import db
from ..models import NGO, Volunteer

registrations_bp = Blueprint("registrations", __name__, url_prefix="/register")


@registrations_bp.post("/ngo")
def register_ngo():
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	email = (data.get("email") or "").strip().lower()
	phone = (data.get("phone") or "").strip()
	if not name or not email or not phone:
		return {"error": "name, email, phone required"}, 400

	# Prevent duplicate email errors
	if NGO.query.filter_by(email=email).first():
		return {"error": "email already registered"}, 409

	ngo = NGO(
		name=name,
		email=email,
		phone=phone,
		location=data.get("location"),
		operating_zones=data.get("operating_zones"),
	)
	db.session.add(ngo)
	db.session.commit()
	return {"message": "NGO registration submitted", "ngo_id": ngo.id}, 201


@registrations_bp.post("/volunteer")
def register_volunteer():
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	email = (data.get("email") or "").strip().lower()
	phone = (data.get("phone") or "").strip()
	if not name or not email or not phone:
		return {"error": "name, email, phone required"}, 400

	if Volunteer.query.filter_by(email=email).first():
		return {"error": "email already registered"}, 409

	vol = Volunteer(
		name=name,
		email=email,
		phone=phone,
		location=data.get("location"),
		expertise=data.get("expertise"),
		availability=data.get("availability"),
	)
	db.session.add(vol)
	db.session.commit()
	return {"message": "Volunteer registration submitted", "volunteer_id": vol.id}, 201
