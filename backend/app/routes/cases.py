from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
from ..extensions import db
from ..models import AnimalCase, CaseStatus, AnimalType
from ..utils import generate_case_code
from ..mailer import send_case_confirmation

cases_bp = Blueprint("cases", __name__, url_prefix="/cases")


@cases_bp.post("")
def report_case():
	# Public endpoint for citizens
	if request.files:
		data = request.form.to_dict()
	else:
		data = request.get_json(silent=True) or {}

	reporter_phone = (data.get("reporter_phone") or "").strip()
	reporter_email = (data.get("reporter_email") or "").strip()
	location = (data.get("location") or "").strip()
	animal_type = (data.get("animal_type") or "Other").title()
	urgency = (data.get("urgency") or "Low").title()
	notes = data.get("notes")

	if not reporter_phone or not location:
		return {"error": "reporter_phone and location are required"}, 400

	try:
		animal_type_enum = AnimalType[animal_type.upper()] if animal_type else AnimalType.OTHER
	except KeyError:
		animal_type_enum = AnimalType.OTHER

	media_url = None
	if "file" in request.files and request.files["file"].filename:
		upload_folder = current_app.config["UPLOAD_FOLDER"]
		os.makedirs(upload_folder, exist_ok=True)
		file = request.files["file"]
		filename = secure_filename(file.filename)
		file.save(os.path.join(upload_folder, filename))
		media_url = f"/uploads/{filename}"

	case = AnimalCase(
		case_code=generate_case_code(),
		reporter_name=data.get("reporter_name"),
		reporter_phone=reporter_phone,
		location=location,
		latitude=float(data.get("latitude")) if data.get("latitude") else None,
		longitude=float(data.get("longitude")) if data.get("longitude") else None,
		animal_type=animal_type_enum,
		urgency=urgency,
		notes=notes,
		media_url=media_url,
	)

	db.session.add(case)
	db.session.commit()

	# Email confirmation (if configured and email provided)
	try:
		if reporter_email:
			send_case_confirmation(reporter_email, case.case_code)
	except Exception:
		pass

	return {"message": "Case reported", "case_id": case.id, "case_code": case.case_code, "media_url": media_url}, 201


@cases_bp.patch("/<int:case_id>/status")
@jwt_required()
def update_status(case_id: int):
	data = request.get_json(silent=True) or {}
	new_status = (data.get("status") or "").upper()
	if new_status not in {s.name for s in CaseStatus}:
		return {"error": "invalid status"}, 400

	case = AnimalCase.query.get_or_404(case_id)
	case.status = CaseStatus[new_status]
	db.session.commit()
	return {"message": "Status updated"}, 200
