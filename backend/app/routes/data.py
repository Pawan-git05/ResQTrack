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

data_bp = Blueprint('data', __name__, url_prefix='/data')

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'csv', 'json'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@data_bp.get('/sample/<path:filename>')
def download_sample_file(filename: str):
    """Serve sample CSV files from the project's sample_data directory."""
    sample_dir = current_app.config.get('SAMPLE_DATA_DIR')
    if not sample_dir:
        # backend/app/routes -> up three levels to project root, then sample_data
        app_root = current_app.root_path
        sample_dir = os.path.abspath(os.path.join(app_root, os.pardir, os.pardir, 'sample_data'))
    return send_from_directory(sample_dir, filename, as_attachment=True)

@data_bp.route('/import/ngos', methods=['POST'])
@jwt_required()
def import_ngos():
    """Import NGOs from CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, f"temp_{filename}")
        file.save(file_path)
        
        # Import data
        importer = DatasetImporter()
        result = importer.import_ngos_csv(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return jsonify({
            'message': 'Import completed',
            'stats': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/import/volunteers', methods=['POST'])
@jwt_required()
def import_volunteers():
    """Import Volunteers from CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, f"temp_{filename}")
        file.save(file_path)
        
        # Import data
        importer = DatasetImporter()
        result = importer.import_volunteers_csv(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return jsonify({
            'message': 'Import completed',
            'stats': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/import/hospitals', methods=['POST'])
@jwt_required()
def import_hospitals():
    """Import Hospitals from CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, f"temp_{filename}")
        file.save(file_path)
        
        # Import data
        importer = DatasetImporter()
        result = importer.import_hospitals_csv(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return jsonify({
            'message': 'Import completed',
            'stats': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/import/police-stations', methods=['POST'])
@jwt_required()
def import_police_stations():
    """Import Police Stations from CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, f"temp_{filename}")
        file.save(file_path)
        
        # Import police stations data
        importer = DatasetImporter()
        result = importer.import_police_stations_csv(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return jsonify({
            'message': 'Import completed',
            'stats': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/import/blood-banks', methods=['POST'])
@jwt_required()
def import_blood_banks():
    """Import Blood Banks from CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, f"temp_{filename}")
        file.save(file_path)
        
        # Import blood banks data
        importer = DatasetImporter()
        result = importer.import_blood_banks_csv(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return jsonify({
            'message': 'Import completed',
            'stats': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/export/ngos', methods=['GET'])
@jwt_required()
def export_ngos():
    """Export NGOs to CSV file"""
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, 'ngos_export.csv')
        
        exporter = DataExporter()
        success = exporter.export_ngos_to_csv(file_path)
        
        if success:
            return jsonify({
                'message': 'Export completed',
                'download_url': f'/uploads/ngos_export.csv'
            }), 200
        else:
            return jsonify({'error': 'Export failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/export/volunteers', methods=['GET'])
@jwt_required()
def export_volunteers():
    """Export Volunteers to CSV file"""
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, 'volunteers_export.csv')
        
        exporter = DataExporter()
        success = exporter.export_volunteers_to_csv(file_path)
        
        if success:
            return jsonify({
                'message': 'Export completed',
                'download_url': f'/uploads/volunteers_export.csv'
            }), 200
        else:
            return jsonify({'error': 'Export failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get data statistics and analytics"""
    try:
        analyzer = DataAnalyzer()
        stats = analyzer.get_import_statistics()
        locations = analyzer.get_location_distribution()
        
        return jsonify({
            'statistics': stats,
            'location_distribution': locations
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/emergency-contacts', methods=['GET'])
def get_emergency_contacts():
    """Get all emergency contacts (public endpoint)"""
    try:
        contacts = EmergencyContact.query.all()
        
        contacts_data = []
        for contact in contacts:
            contacts_data.append({
                'id': contact.id,
                'name': contact.name,
                'phone': contact.phone,
                'email': contact.email,
                'service_type': contact.service_type,
                'location': contact.location,
                'is_24x7': contact.is_24x7,
                'description': contact.description,
                'priority_level': contact.priority_level
            })
        
        return jsonify({'contacts': contacts_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/emergency-contacts', methods=['POST'])
@jwt_required()
def create_emergency_contact():
    """Create a new emergency contact"""
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
        
        return jsonify({
            'message': 'Emergency contact created successfully',
            'id': contact.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@data_bp.route('/nearby-services', methods=['GET'])
def get_nearby_services():
    """Get nearby emergency services based on location"""
    try:
        location = request.args.get('location')
        service_type = request.args.get('service_type')  # hospital, police, fire, blood_bank
        
        if not location:
            return jsonify({'error': 'Location parameter is required'}), 400
        
        services = []
        
        if service_type == 'hospital' or not service_type:
            hospitals = Hospital.query.filter(Hospital.location.contains(location)).all()
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
        
        if service_type == 'police' or not service_type:
            police_stations = PoliceStation.query.filter(PoliceStation.location.contains(location)).all()
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
        
        if service_type == 'fire' or not service_type:
            fire_stations = FireStation.query.filter(FireStation.location.contains(location)).all()
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
        
        if service_type == 'blood_bank' or not service_type:
            blood_banks = BloodBank.query.filter(BloodBank.location.contains(location)).all()
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


@data_bp.route('/delete-entry/<service_type>/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_entry(service_type, entry_id):
    """Delete a specific entry from any service type"""
    try:
        if service_type == 'hospital':
            entry = Hospital.query.get_or_404(entry_id)
        elif service_type == 'police':
            entry = PoliceStation.query.get_or_404(entry_id)
        elif service_type == 'fire':
            entry = FireStation.query.get_or_404(entry_id)
        elif service_type == 'blood_bank':
            entry = BloodBank.query.get_or_404(entry_id)
        elif service_type == 'ngo':
            entry = NGO.query.get_or_404(entry_id)
        elif service_type == 'volunteer':
            entry = Volunteer.query.get_or_404(entry_id)
        elif service_type == 'emergency_contact':
            entry = EmergencyContact.query.get_or_404(entry_id)
        else:
            return jsonify({'error': 'Invalid service type'}), 400
        
        db.session.delete(entry)
        db.session.commit()
        
        return jsonify({'message': f'{service_type.title()} entry deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@data_bp.route('/clear-data/<service_type>', methods=['DELETE'])
@jwt_required()
def clear_data(service_type):
    """Clear all data for a specific service type"""
    try:
        if service_type == 'hospitals':
            Hospital.query.delete()
        elif service_type == 'police-stations':
            PoliceStation.query.delete()
        elif service_type == 'fire-stations':
            FireStation.query.delete()
        elif service_type == 'blood-banks':
            BloodBank.query.delete()
        elif service_type == 'ngos':
            NGO.query.delete()
        elif service_type == 'volunteers':
            Volunteer.query.delete()
        elif service_type == 'emergency-contacts':
            EmergencyContact.query.delete()
        else:
            return jsonify({'error': 'Invalid service type'}), 400
        
        db.session.commit()
        
        return jsonify({'message': f'All {service_type} data cleared successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@data_bp.route('/uploaded-files', methods=['GET'])
@jwt_required()
def list_uploaded_files():
    """List all uploaded CSV files"""
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        files = []
        for filename in os.listdir(upload_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(upload_folder, filename)
                file_stat = os.stat(file_path)
                files.append({
                    'name': filename,
                    'size': file_stat.st_size,
                    'modified': file_stat.st_mtime,
                    'path': file_path
                })
        
        return jsonify({'files': files}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/delete-file', methods=['DELETE'])
@jwt_required()
def delete_uploaded_file():
    """Delete an uploaded CSV file"""
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