from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import (
    AnimalCase, NGO, Volunteer, Donation, Hospital, CaseStatus,
    PoliceStation, BloodBank, FireStation, EmergencyContact
)
import csv
import io
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/cases")
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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


@admin_bp.get("/police-stations")
@jwt_required()
def get_all_police_stations():
	"""Get all police stations for admin dashboard"""
	stations = PoliceStation.query.order_by(PoliceStation.created_at.desc()).all()
	return {
		"police_stations": [
			{
				"id": station.id,
				"name": station.name,
				"address": station.address,
				"phone": station.phone,
				"location": station.location,
				"station_code": station.station_code,
				"is_24x7": station.is_24x7,
				"jurisdiction": station.jurisdiction,
				"officer_in_charge": station.officer_in_charge,
				"created_at": station.created_at.isoformat() if station.created_at else None,
				"updated_at": station.updated_at.isoformat() if station.updated_at else None,
			}
			for station in stations
		]
	}


@admin_bp.get("/blood-banks")
@jwt_required()
def get_all_blood_banks():
	"""Get all blood banks for admin dashboard"""
	banks = BloodBank.query.order_by(BloodBank.created_at.desc()).all()
	return {
		"blood_banks": [
			{
				"id": bank.id,
				"name": bank.name,
				"address": bank.address,
				"phone": bank.phone,
				"location": bank.location,
				"is_24x7": bank.is_24x7,
				"blood_types_available": bank.blood_types_available,
				"contact_person": bank.contact_person,
				"license_number": bank.license_number,
				"created_at": bank.created_at.isoformat() if bank.created_at else None,
				"updated_at": bank.updated_at.isoformat() if bank.updated_at else None,
			}
			for bank in banks
		]
	}


@admin_bp.get("/fire-stations")
@jwt_required()
def get_all_fire_stations():
	"""Get all fire stations for admin dashboard"""
	stations = FireStation.query.order_by(FireStation.created_at.desc()).all()
	return {
		"fire_stations": [
			{
				"id": station.id,
				"name": station.name,
				"address": station.address,
				"phone": station.phone,
				"location": station.location,
				"station_code": station.station_code,
				"is_24x7": station.is_24x7,
				"equipment_available": station.equipment_available,
				"chief_officer": station.chief_officer,
				"created_at": station.created_at.isoformat() if station.created_at else None,
				"updated_at": station.updated_at.isoformat() if station.updated_at else None,
			}
			for station in stations
		]
	}


@admin_bp.get("/emergency-contacts")
@jwt_required()
def get_all_emergency_contacts():
	"""Get all emergency contacts for admin dashboard"""
	contacts = EmergencyContact.query.order_by(EmergencyContact.created_at.desc()).all()
	return {
		"emergency_contacts": [
			{
				"id": contact.id,
				"name": contact.name,
				"phone": contact.phone,
				"email": contact.email,
				"service_type": contact.service_type,
				"location": contact.location,
				"is_24x7": contact.is_24x7,
				"description": contact.description,
				"priority_level": contact.priority_level,
				"created_at": contact.created_at.isoformat() if contact.created_at else None,
				"updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
			}
			for contact in contacts
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


@admin_bp.post("/hospitals")
@jwt_required()
def add_hospital():
	"""Add a new hospital"""
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	if not name:
		return {"error": "name required"}, 400

	hospital = Hospital(
		name=name,
		address=data.get("address"),
		phone=data.get("phone"),
		location=data.get("location"),
		is_24x7=bool(data.get("is_24x7", False)),
		treatment_types=data.get("treatment_types"),
	)
	db.session.add(hospital)
	db.session.commit()
	return {"message": "Hospital added successfully", "id": hospital.id}, 201


@admin_bp.post("/police-stations")
@jwt_required()
def add_police_station():
	"""Add a new police station"""
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	if not name:
		return {"error": "name required"}, 400

	station = PoliceStation(
		name=name,
		address=data.get("address"),
		phone=data.get("phone"),
		location=data.get("location"),
		station_code=data.get("station_code"),
		is_24x7=bool(data.get("is_24x7", True)),
		jurisdiction=data.get("jurisdiction"),
		officer_in_charge=data.get("officer_in_charge"),
	)
	db.session.add(station)
	db.session.commit()
	return {"message": "Police station added successfully", "id": station.id}, 201


@admin_bp.post("/blood-banks")
@jwt_required()
def add_blood_bank():
	"""Add a new blood bank"""
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	if not name:
		return {"error": "name required"}, 400

	bank = BloodBank(
		name=name,
		address=data.get("address"),
		phone=data.get("phone"),
		location=data.get("location"),
		is_24x7=bool(data.get("is_24x7", False)),
		blood_types_available=data.get("blood_types_available"),
		contact_person=data.get("contact_person"),
		license_number=data.get("license_number"),
	)
	db.session.add(bank)
	db.session.commit()
	return {"message": "Blood bank added successfully", "id": bank.id}, 201


@admin_bp.post("/fire-stations")
@jwt_required()
def add_fire_station():
	"""Add a new fire station"""
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	if not name:
		return {"error": "name required"}, 400

	station = FireStation(
		name=name,
		address=data.get("address"),
		phone=data.get("phone"),
		location=data.get("location"),
		station_code=data.get("station_code"),
		is_24x7=bool(data.get("is_24x7", True)),
		equipment_available=data.get("equipment_available"),
		chief_officer=data.get("chief_officer"),
	)
	db.session.add(station)
	db.session.commit()
	return {"message": "Fire station added successfully", "id": station.id}, 201


@admin_bp.post("/emergency-contacts")
@jwt_required()
def add_emergency_contact():
	"""Add a new emergency contact"""
	data = request.get_json(silent=True) or {}
	name = (data.get("name") or "").strip()
	phone = (data.get("phone") or "").strip()
	service_type = (data.get("service_type") or "").strip()
	
	if not name or not phone or not service_type:
		return {"error": "name, phone, and service_type required"}, 400

	contact = EmergencyContact(
		name=name,
		phone=phone,
		email=data.get("email"),
		service_type=service_type,
		location=data.get("location"),
		is_24x7=bool(data.get("is_24x7", True)),
		description=data.get("description"),
		priority_level=int(data.get("priority_level", 1))
	)
	db.session.add(contact)
	db.session.commit()
	return {"message": "Emergency contact added successfully", "id": contact.id}, 201


@admin_bp.post("/upload-csv/<service_type>")
@jwt_required()
def upload_csv(service_type: str):
	"""Upload and import CSV data for emergency services"""
	if 'file' not in request.files:
		return {"error": "No file provided"}, 400
	
	file = request.files['file']
	if file.filename == '':
		return {"error": "No file selected"}, 400
	
	if not file.filename.lower().endswith('.csv'):
		return {"error": "File must be a CSV"}, 400
	
	try:
		# Read CSV content
		stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
		csv_input = csv.DictReader(stream)
		
		imported_count = 0
		errors = []
		
		if service_type == 'police-stations':
			imported_count, errors = _import_police_stations(csv_input)
		elif service_type == 'blood-banks':
			imported_count, errors = _import_blood_banks(csv_input)
		elif service_type == 'fire-stations':
			imported_count, errors = _import_fire_stations(csv_input)
		elif service_type == 'emergency-contacts':
			imported_count, errors = _import_emergency_contacts(csv_input)
		elif service_type == 'hospitals':
			imported_count, errors = _import_hospitals(csv_input)
		else:
			return {"error": "Invalid service type"}, 400
		
		return {
			"message": f"Successfully imported {imported_count} records",
			"imported_count": imported_count,
			"errors": errors
		}, 200
		
	except Exception as e:
		return {"error": f"Failed to process CSV: {str(e)}"}, 500


def _import_police_stations(csv_input):
	"""Import police stations from CSV"""
	imported_count = 0
	errors = []
	
	for row_num, row in enumerate(csv_input, 1):
		try:
			station = PoliceStation(
				name=row.get('name', '').strip(),
				address=row.get('address', '').strip() or None,
				phone=row.get('phone', '').strip() or None,
				location=row.get('location', '').strip() or None,
				station_code=row.get('station_code', '').strip() or None,
				is_24x7=row.get('is_24x7', '').lower() in ['true', '1', 'yes', 'y'],
				jurisdiction=row.get('jurisdiction', '').strip() or None,
				officer_in_charge=row.get('officer_in_charge', '').strip() or None
			)
			db.session.add(station)
			imported_count += 1
		except Exception as e:
			errors.append(f"Row {row_num}: {str(e)}")
	
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		errors.append(f"Database error: {str(e)}")
		imported_count = 0
	
	return imported_count, errors


def _import_blood_banks(csv_input):
	"""Import blood banks from CSV"""
	imported_count = 0
	errors = []
	
	for row_num, row in enumerate(csv_input, 1):
		try:
			bank = BloodBank(
				name=row.get('name', '').strip(),
				address=row.get('address', '').strip() or None,
				phone=row.get('phone', '').strip() or None,
				location=row.get('location', '').strip() or None,
				is_24x7=row.get('is_24x7', '').lower() in ['true', '1', 'yes', 'y'],
				blood_types_available=row.get('blood_types_available', '').strip() or None,
				contact_person=row.get('contact_person', '').strip() or None,
				license_number=row.get('license_number', '').strip() or None
			)
			db.session.add(bank)
			imported_count += 1
		except Exception as e:
			errors.append(f"Row {row_num}: {str(e)}")
	
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		errors.append(f"Database error: {str(e)}")
		imported_count = 0
	
	return imported_count, errors


def _import_fire_stations(csv_input):
	"""Import fire stations from CSV"""
	imported_count = 0
	errors = []
	
	for row_num, row in enumerate(csv_input, 1):
		try:
			station = FireStation(
				name=row.get('name', '').strip(),
				address=row.get('address', '').strip() or None,
				phone=row.get('phone', '').strip() or None,
				location=row.get('location', '').strip() or None,
				station_code=row.get('station_code', '').strip() or None,
				is_24x7=row.get('is_24x7', '').lower() in ['true', '1', 'yes', 'y'],
				equipment_available=row.get('equipment_available', '').strip() or None,
				chief_officer=row.get('chief_officer', '').strip() or None
			)
			db.session.add(station)
			imported_count += 1
		except Exception as e:
			errors.append(f"Row {row_num}: {str(e)}")
	
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		errors.append(f"Database error: {str(e)}")
		imported_count = 0
	
	return imported_count, errors


def _import_emergency_contacts(csv_input):
	"""Import emergency contacts from CSV"""
	imported_count = 0
	errors = []
	
	for row_num, row in enumerate(csv_input, 1):
		try:
			contact = EmergencyContact(
				name=row.get('name', '').strip(),
				phone=row.get('phone', '').strip(),
				email=row.get('email', '').strip() or None,
				service_type=row.get('service_type', '').strip(),
				location=row.get('location', '').strip() or None,
				is_24x7=row.get('is_24x7', '').lower() in ['true', '1', 'yes', 'y'],
				description=row.get('description', '').strip() or None,
				priority_level=int(row.get('priority_level', '1'))
			)
			db.session.add(contact)
			imported_count += 1
		except Exception as e:
			errors.append(f"Row {row_num}: {str(e)}")
	
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		errors.append(f"Database error: {str(e)}")
		imported_count = 0
	
	return imported_count, errors


def _import_hospitals(csv_input):
	"""Import hospitals from CSV"""
	imported_count = 0
	errors = []
	
	for row_num, row in enumerate(csv_input, 1):
		try:
			hospital = Hospital(
				name=row.get('name', '').strip(),
				address=row.get('address', '').strip() or None,
				phone=row.get('phone', '').strip() or None,
				location=row.get('location', '').strip() or None,
				is_24x7=row.get('is_24x7', '').lower() in ['true', '1', 'yes', 'y'],
				treatment_types=row.get('treatment_types', '').strip() or None
			)
			db.session.add(hospital)
			imported_count += 1
		except Exception as e:
			errors.append(f"Row {row_num}: {str(e)}")
	
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		errors.append(f"Database error: {str(e)}")
		imported_count = 0
	
	return imported_count, errors
