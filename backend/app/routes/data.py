"""
Data Import/Export API Routes for ResQTrack
Handles CSV uploads, data validation, and export functionality
"""

import os
import json
from flask import Blueprint, request, jsonify, current_app, send_from_directory

from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import NGO, Volunteer, Hospital, PoliceStation, BloodBank, FireStation, EmergencyContact
from ..data_integration import DatasetImporter, DataExporter, DataAnalyzer

# -----------------------
# Blueprint
# -----------------------
data_bp = Blueprint('data', __name__, url_prefix='/data')

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'csv', 'json'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------
# Sample file download
# -----------------------
@data_bp.get('/sample/<path:filename>')
def download_sample_file(filename: str):
    sample_dir = current_app.config.get('SAMPLE_DATA_DIR')

    if not sample_dir:
        app_root = current_app.root_path
        sample_dir = os.path.abspath(os.path.join(app_root, os.pardir, os.pardir, 'sample_data'))

    return send_from_directory(sample_dir, filename, as_attachment=True)


# -----------------------
# Import dataset
# -----------------------
@data_bp.route('/import/<dataset_type>', methods=['POST'])
def import_dataset(dataset_type):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV and JSON are allowed.'}), 400

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, f"temp_{filename}")
        file.save(file_path)

        # Import data
        importer = DatasetImporter()

        ALLOWED_DATASETS = {
            'ngos': importer.import_ngos_csv,
            'volunteers': importer.import_volunteers_csv,
            'hospitals': importer.import_hospitals_csv,
            'police-stations': importer.import_police_stations_csv,
            'blood-banks': importer.import_blood_banks_csv,
        }

        if dataset_type not in ALLOWED_DATASETS:
            return jsonify({'error': 'Invalid dataset type'}), 400

        importer_method = ALLOWED_DATASETS[dataset_type]
        result = importer_method(file_path)

        os.remove(file_path)

        return jsonify({'message': 'Import completed', 'stats': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------
# Export NGOs
# -----------------------
@data_bp.route('/export/ngos', methods=['GET'])
def export_ngos():
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, 'ngos_export.csv')

        exporter = DataExporter()
        success = exporter.export_ngos_to_csv(file_path)

        if success:
            return jsonify({'message': 'Export completed', 'download_url': f'/uploads/ngos_export.csv'}), 200
        else:
            return jsonify({'error': 'Export failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------
# Export Volunteers
# -----------------------
@data_bp.route('/export/volunteers', methods=['GET'])
def export_volunteers():
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, 'volunteers_export.csv')

        exporter = DataExporter()
        success = exporter.export_volunteers_to_csv(file_path)

        if success:
            return jsonify({'message': 'Export completed', 'download_url': f'/uploads/volunteers_export.csv'}), 200
        else:
            return jsonify({'error': 'Export failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------
# Stats
# -----------------------
@data_bp.route('/stats', methods=['GET'])
def get_statistics():
    try:
        analyzer = DataAnalyzer()
        stats = analyzer.get_import_statistics()
        locations = analyzer.get_location_distribution()

        return jsonify({'statistics': stats, 'location_distribution': locations}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------
# Emergency Contacts
# -----------------------
@data_bp.route('/emergency-contacts', methods=['GET'])
def get_emergency_contacts():
    try:
        contacts = EmergencyContact.query.all()

        contacts_data = [
            {
                'id': c.id,
                'name': c.name,
                'phone': c.phone,
                'email': c.email,
                'service_type': c.service_type,
                'location': c.location,
                'is_24x7': c.is_24x7,
                'description': c.description,
                'priority_level': c.priority_level
            }
            for c in contacts
        ]

        return jsonify({'contacts': contacts_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/emergency-contacts', methods=['POST'])
def create_emergency_contact():
    try:
        data = request.get_json()

        contact = EmergencyContact(
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email'),
            service_type=data.get('service_type'),
            location=data.get('location'),
            is_24x7=data.get('is_24x7', True),
            description=data.get('description'),
            priority_level=data.get('priority_level', 1)
        )

        db.session.add(contact)
        db.session.commit()

        return jsonify({'message': 'Emergency contact created successfully', 'id': contact.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# -----------------------
# Emergency Services
# -----------------------
@data_bp.route('/emergency-services', methods=['GET'])
def get_emergency_services():
    try:
        services = []

        hospitals = Hospital.query.all()
        for hospital in hospitals:
            services.append({
                'type': 'hospital',
                'id': hospital.id,
                'name': hospital.name,
                'address': hospital.address,
                'phone': hospital.phone,
                'location': hospital.location,
                'is_24x7': hospital.is_24x7,
                'treatment_types': hospital.treatment_types
            })

        police_stations = PoliceStation.query.all()
        for station in police_stations:
            services.append({
                'type': 'police',
                'id': station.id,
                'name': station.name,
                'address': station.address,
                'phone': station.phone,
                'location': station.location,
                'is_24x7': station.is_24x7,
                'station_code': station.station_code
            })

        fire_stations = FireStation.query.all()
        for station in fire_stations:
            services.append({
                'type': 'fire',
                'id': station.id,
                'name': station.name,
                'address': station.address,
                'phone': station.phone,
                'location': station.location,
                'is_24x7': station.is_24x7,
                'station_code': station.station_code
            })

        blood_banks = BloodBank.query.all()
        for bank in blood_banks:
            services.append({
                'type': 'blood_bank',
                'id': bank.id,
                'name': bank.name,
                'address': bank.address,
                'phone': bank.phone,
                'location': bank.location,
                'is_24x7': bank.is_24x7,
                'contact_person': bank.contact_person
            })

        return jsonify({'services': services}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------
# Clear Data
# -----------------------
@data_bp.route('/clear-data/<service_type>', methods=['DELETE'])
def clear_data(service_type):
    try:
        mapping = {
            'hospitals': Hospital,
            'police-stations': PoliceStation,
            'fire-stations': FireStation,
            'blood-banks': BloodBank,
            'ngos': NGO,
            'volunteers': Volunteer,
            'emergency-contacts': EmergencyContact,
        }

        if service_type not in mapping:
            return jsonify({'error': 'Invalid service type'}), 400

        mapping[service_type].query.delete()
        db.session.commit()

        return jsonify({'message': f'All {service_type} data cleared successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# -----------------------
# List Uploaded Files
# -----------------------
@data_bp.route('/files', methods=['GET'])
def list_uploaded_files():
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        files = []
        for filename in os.listdir(upload_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(upload_folder, filename)
                stat = os.stat(file_path)

                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'path': file_path
                })

        return jsonify({'files': files}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------
# Delete File
# -----------------------
@data_bp.route('/delete-file', methods=['DELETE'])
def delete_uploaded_file():
    try:
        data = request.get_json()
        filename = data.get('filename')

        if not filename:
            return jsonify({'error': 'Filename is required'}), 400

        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        file_path = os.path.join(upload_folder, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': f'File {filename} deleted successfully'}), 200
        else:
            return jsonify({'error': 'File not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
