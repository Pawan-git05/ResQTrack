from flask import Blueprint, request, Response
from ..extensions import db
from ..models import (
    AnimalCase, NGO, Volunteer, Donation, Hospital, CaseStatus,
    PoliceStation, BloodBank, FireStation, EmergencyContact
)
import csv
import io

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================
#  GET ENDPOINTS (NO JWT)
# =========================

@admin_bp.get("/cases")
def get_all_cases():
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
                "created_at": ngo.created_at.isoformat(),
                "updated_at": ngo.updated_at.isoformat(),
            }
            for ngo in ngos
        ]
    }


@admin_bp.get("/volunteers")
def get_all_volunteers():
    volunteers = Volunteer.query.order_by(Volunteer.created_at.desc()).all()
    return {
        "volunteers": [
            {
                "id": v.id,
                "name": v.name,
                "email": v.email,
                "phone": v.phone,
                "location": v.location,
                "expertise": v.expertise,
                "availability": v.availability,
                "approved": v.approved,
                "ngo_id": v.ngo_id,
                "created_at": v.created_at.isoformat(),
                "updated_at": v.updated_at.isoformat(),
            }
            for v in volunteers
        ]
    }


@admin_bp.get("/donations")
def get_all_donations():
    donations = Donation.query.order_by(Donation.created_at.desc()).all()
    return {
        "donations": [
            {
                "id": d.id,
                "donor_name": d.donor_name,
                "donor_email": d.donor_email,
                "amount": float(d.amount or 0),
                "currency": d.currency,
                "category": d.category,
                "payment_provider": d.payment_provider,
                "payment_id": d.payment_id,
                "ngo_id": d.ngo_id,
                "created_at": d.created_at.isoformat(),
                "updated_at": d.updated_at.isoformat(),
            }
            for d in donations
        ]
    }


@admin_bp.get("/hospitals")
def get_all_hospitals():
    hospitals = Hospital.query.order_by(Hospital.created_at.desc()).all()
    return {
        "hospitals": [
            {
                "id": h.id,
                "name": h.name,
                "address": h.address,
                "phone": h.phone,
                "location": h.location,
                "is_24x7": h.is_24x7,
                "treatment_types": h.treatment_types,
                "created_at": h.created_at.isoformat(),
                "updated_at": h.updated_at.isoformat(),
            }
            for h in hospitals
        ]
    }


# =========================
#  STATUS / APPROVAL
# =========================

@admin_bp.patch("/ngos/<int:ngo_id>/approve")
def approve_ngo(ngo_id):
    ngo = NGO.query.get_or_404(ngo_id)
    ngo.approved = True
    db.session.commit()
    return {"message": "NGO approved"}, 200


@admin_bp.patch("/volunteers/<int:vid>/approve")
def approve_volunteer(vid):
    v = Volunteer.query.get_or_404(vid)
    v.approved = True
    db.session.commit()
    return {"message": "Volunteer approved"}, 200


# =========================
#  CSV UPLOAD (FIXED)
# =========================

@admin_bp.route("/upload-csv/<service_type>", methods=["POST", "OPTIONS"])
def upload_csv(service_type):
    if request.method == "OPTIONS":
        return ("", 200)

    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files["file"]

    if not file.filename.lower().endswith(".csv"):
        return {"error": "Must upload CSV"}, 400

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        csv_input = csv.DictReader(stream)

        if service_type == "hospitals":
            imported, errors = _import_hospitals(csv_input)

        elif service_type == "blood-banks":
            imported, errors = _import_blood_banks(csv_input)

        elif service_type == "police-stations":
            imported, errors = _import_police_stations(csv_input)

        elif service_type == "fire-stations":
            imported, errors = _import_fire_stations(csv_input)

        elif service_type == "emergency-contacts":
            imported, errors = _import_emergency_contacts(csv_input)

        else:
            return {"error": "Invalid service type"}, 400

        return {
            "message": f"Imported {imported} records",
            "errors": errors
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500


# =========================
#  SAMPLE CSV DOWNLOAD
# =========================

@admin_bp.get("/sample-csv/<service_type>")
def download_sample_csv(service_type):
    headers = {
        "hospitals": ["name", "address", "phone", "location", "is_24x7", "treatment_types"],
        "blood-banks": ["name", "address", "phone", "location", "is_24x7", "blood_types_available", "contact_person", "license_number"],
        "police-stations": ["name", "address", "phone", "location", "station_code", "is_24x7", "jurisdiction", "officer_in_charge"],
        "fire-stations": ["name", "address", "phone", "location", "station_code", "is_24x7", "equipment_available", "chief_officer"],
        "emergency-contacts": ["name", "phone", "email", "service_type", "location", "is_24x7", "description", "priority_level"]
    }

    if service_type not in headers:
        return {"error": "Invalid service type"}, 400

    output = io.StringIO()
    cw = csv.writer(output)
    cw.writerow(headers[service_type])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=sample_{service_type}.csv"}
    )


# =========================
#  CSV IMPORT FUNCTIONS
# =========================

def _import_hospitals(rows):
    imported = 0
    errors = []
    for n, row in enumerate(rows, 1):
        try:
            obj = Hospital(
                name=row.get("name", "").strip(),
                address=row.get("address"),
                phone=row.get("phone"),
                location=row.get("location"),
                is_24x7=row.get("is_24x7", "").lower() in ["true", "1", "yes"],
                treatment_types=row.get("treatment_types")
            )
            db.session.add(obj)
            imported += 1
        except Exception as e:
            errors.append(f"Row {n}: {str(e)}")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return 0, [str(e)]

    return imported, errors


# (same for other importers — unchanged)
