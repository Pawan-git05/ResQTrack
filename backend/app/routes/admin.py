from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import AnimalCase, NGO, Volunteer, Donation, Hospital, CaseStatus

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/cases")
def get_all_cases():
	"""Get all animal cases for admin dashboard"""
	cases = AnimalCase.query.order_by(AnimalCase.created_at.desc()).all()
	return {
		"cases": [
			{
				"id": case.id,
				"case_code": case.case_code,
				"reporter_name": case.reporter_name,
				"reporter_phone": case.reporter_phone,
				"location": case.location,
				"animal_type": case.animal_type.value if case.animal_type else "Other",
				"urgency": case.urgency,
				"status": case.status.value if case.status else "PENDING",
				"notes": case.notes,
				"media_url": case.media_url,
				"created_at": case.created_at.isoformat() if case.created_at else None,
				"updated_at": case.updated_at.isoformat() if case.updated_at else None,
			}
			for case in cases
		]
	}


@admin_bp.get("/ngos")
def get_all_ngos():
	"""Get all NGOs for admin dashboard"""
	ngos = NGO.query.order_by(NGO.created_at.desc()).all()
	return {
		"ngos": [
			{
				"id": ngo.id,
				"name": ngo.name,
				"email": ngo.email,
				"phone": ngo.phone,
				"location": ngo.location,
				"operating_zones": ngo.operating_zones,
				"approved": ngo.approved,
				"created_at": ngo.created_at.isoformat() if ngo.created_at else None,
				"updated_at": ngo.updated_at.isoformat() if ngo.updated_at else None,
			}
			for ngo in ngos
		]
	}


@admin_bp.get("/volunteers")
def get_all_volunteers():
	"""Get all volunteers for admin dashboard"""
	volunteers = Volunteer.query.order_by(Volunteer.created_at.desc()).all()
	return {
		"volunteers": [
			{
				"id": vol.id,
				"name": vol.name,
				"email": vol.email,
				"phone": vol.phone,
				"location": vol.location,
				"expertise": vol.expertise,
				"availability": vol.availability,
				"approved": vol.approved,
				"ngo_id": vol.ngo_id,
				"created_at": vol.created_at.isoformat() if vol.created_at else None,
				"updated_at": vol.updated_at.isoformat() if vol.updated_at else None,
			}
			for vol in volunteers
		]
	}


@admin_bp.get("/donations")
def get_all_donations():
	"""Get all donations for admin dashboard"""
	donations = Donation.query.order_by(Donation.created_at.desc()).all()
	return {
		"donations": [
			{
				"id": donation.id,
				"donor_name": donation.donor_name,
				"donor_email": donation.donor_email,
				"amount": float(donation.amount) if donation.amount else 0,
				"currency": donation.currency,
				"category": donation.category,
				"payment_provider": donation.payment_provider,
				"payment_id": donation.payment_id,
				"ngo_id": donation.ngo_id,
				"created_at": donation.created_at.isoformat() if donation.created_at else None,
				"updated_at": donation.updated_at.isoformat() if donation.updated_at else None,
			}
			for donation in donations
		]
	}


@admin_bp.get("/hospitals")
def get_all_hospitals():
	"""Get all hospitals for admin dashboard"""
	hospitals = Hospital.query.order_by(Hospital.created_at.desc()).all()
	return {
		"hospitals": [
			{
				"id": hospital.id,
				"name": hospital.name,
				"address": hospital.address,
				"phone": hospital.phone,
				"location": hospital.location,
				"is_24x7": hospital.is_24x7,
				"treatment_types": hospital.treatment_types,
				"created_at": hospital.created_at.isoformat() if hospital.created_at else None,
				"updated_at": hospital.updated_at.isoformat() if hospital.updated_at else None,
			}
			for hospital in hospitals
		]
	}


@admin_bp.patch("/ngos/<int:ngo_id>/approve")
@jwt_required()
def approve_ngo(ngo_id: int):
	"""Approve an NGO registration"""
	ngo = NGO.query.get_or_404(ngo_id)
	ngo.approved = True
	db.session.commit()
	return {"message": "NGO approved successfully"}, 200


@admin_bp.patch("/volunteers/<int:volunteer_id>/approve")
@jwt_required()
def approve_volunteer(volunteer_id: int):
	"""Approve a volunteer registration"""
	volunteer = Volunteer.query.get_or_404(volunteer_id)
	volunteer.approved = True
	db.session.commit()
	return {"message": "Volunteer approved successfully"}, 200


@admin_bp.patch("/cases/<int:case_id>/status")
@jwt_required()
def update_case_status(case_id: int):
	"""Update case status"""
	data = request.get_json(silent=True) or {}
	new_status = (data.get("status") or "").upper()
	
	if new_status not in {s.name for s in CaseStatus}:
		return {"error": "invalid status"}, 400

	case = AnimalCase.query.get_or_404(case_id)
	case.status = CaseStatus[new_status]
	db.session.commit()
	return {"message": "Case status updated successfully"}, 200
