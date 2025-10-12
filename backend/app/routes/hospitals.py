from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Hospital

hospitals_bp = Blueprint("hospitals", __name__, url_prefix="/hospitals")


@hospitals_bp.get("")
def list_hospitals():
	hospitals = Hospital.query.order_by(Hospital.name.asc()).all()
	return {
		"items": [
			{
				"id": h.id,
				"name": h.name,
				"address": h.address,
				"phone": h.phone,
				"location": h.location,
				"is_24x7": h.is_24x7,
				"treatment_types": h.treatment_types,
			}
			for h in hospitals
		]
	}


@hospitals_bp.post("")
@jwt_required()
def add_hospital():
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	if not name:
		return {"error": "name required"}, 400

	h = Hospital(
		name=name,
		address=data.get("address"),
		phone=data.get("phone"),
		location=data.get("location"),
		is_24x7=bool(data.get("is_24x7", False)),
		treatment_types=data.get("treatment_types"),
	)
	db.session.add(h)
	db.session.commit()
	return {"message": "Hospital added", "id": h.id}, 201
