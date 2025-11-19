"""
Data Integration Module for ResQTrack
Handles importing and managing multiple real-world datasets
"""

import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from .extensions import db
from .models import NGO, Volunteer, Hospital, PoliceStation, BloodBank, FireStation, EmergencyContact


class DataValidator:
    """Validates data before import"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        return email and '@' in email and '.' in email.split('@')[-1]
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Basic phone validation"""
        return phone and len(phone.replace(' ', '').replace('-', '').replace('+', '')) >= 10
    
    @staticmethod
    def validate_location(location: str) -> bool:
        """Basic location validation"""
        return location and len(location.strip()) > 3


class DatasetImporter:
    """Handles importing various dataset types"""
    
    def __init__(self):
        self.validator = DataValidator()
        self.import_stats = {
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
    
    def import_ngos_csv(self, file_path: str) -> Dict[str, Any]:
        """Import NGOs from CSV file"""
        self.import_stats = {'successful': 0, 'failed': 0, 'skipped': 0, 'errors': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Map CSV columns to database fields
                        ngo_data = {
                            'name': row.get('name', '').strip(),
                            'email': row.get('email', '').strip().lower(),
                            'phone': row.get('phone', '').strip(),
                            'location': row.get('location', '').strip(),
                            'operating_zones': row.get('operating_zones', '').strip(),
                            'approved': row.get('approved', 'false').lower() == 'true'
                        }
                        
                        # Validate required fields
                        if not ngo_data['name'] or not ngo_data['email']:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Missing name or email")
                            continue
                        
                        if not self.validator.validate_email(ngo_data['email']):
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Invalid email format")
                            continue
                        
                        # Check if NGO already exists
                        existing_ngo = NGO.query.filter_by(email=ngo_data['email']).first()
                        if existing_ngo:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: NGO with email {ngo_data['email']} already exists")
                            continue
                        
                        # Create new NGO
                        ngo = NGO(**ngo_data)
                        db.session.add(ngo)
                        self.import_stats['successful'] += 1
                        
                    except Exception as e:
                        self.import_stats['failed'] += 1
                        self.import_stats['errors'].append(f"Row {row_num}: {str(e)}")
                
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            self.import_stats['errors'].append(f"File error: {str(e)}")
        
        return self.import_stats
    
    def import_volunteers_csv(self, file_path: str) -> Dict[str, Any]:
        """Import Volunteers from CSV file"""
        self.import_stats = {'successful': 0, 'failed': 0, 'skipped': 0, 'errors': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Map CSV columns to database fields
                        volunteer_data = {
                            'name': row.get('name', '').strip(),
                            'email': row.get('email', '').strip().lower(),
                            'phone': row.get('phone', '').strip(),
                            'location': row.get('location', '').strip(),
                            'expertise': row.get('expertise', '').strip(),
                            'availability': row.get('availability', '').strip(),
                            'approved': row.get('approved', 'false').lower() == 'true'
                        }
                        
                        # Validate required fields
                        if not volunteer_data['name'] or not volunteer_data['email']:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Missing name or email")
                            continue
                        
                        if not self.validator.validate_email(volunteer_data['email']):
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Invalid email format")
                            continue
                        
                        # Check if volunteer already exists
                        existing_volunteer = Volunteer.query.filter_by(email=volunteer_data['email']).first()
                        if existing_volunteer:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Volunteer with email {volunteer_data['email']} already exists")
                            continue
                        
                        # Create new volunteer
                        volunteer = Volunteer(**volunteer_data)
                        db.session.add(volunteer)
                        self.import_stats['successful'] += 1
                        
                    except Exception as e:
                        self.import_stats['failed'] += 1
                        self.import_stats['errors'].append(f"Row {row_num}: {str(e)}")
                
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            self.import_stats['errors'].append(f"File error: {str(e)}")
        
        return self.import_stats
    
    def import_hospitals_csv(self, file_path: str) -> Dict[str, Any]:
        """Import Hospitals from CSV file"""
        self.import_stats = {'successful': 0, 'failed': 0, 'skipped': 0, 'errors': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Map CSV columns to database fields
                        hospital_data = {
                            'name': row.get('name', '').strip(),
                            'address': row.get('address', '').strip(),
                            'phone': row.get('phone', '').strip(),
                            'location': row.get('location', '').strip(),
                            'is_24x7': row.get('is_24x7', 'false').lower() == 'true',
                            'treatment_types': row.get('treatment_types', '').strip()
                        }
                        
                        # Validate required fields
                        if not hospital_data['name']:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Missing hospital name")
                            continue
                        
                        # Create new hospital
                        hospital = Hospital(**hospital_data)
                        db.session.add(hospital)
                        self.import_stats['successful'] += 1
                        
                    except Exception as e:
                        self.import_stats['failed'] += 1
                        self.import_stats['errors'].append(f"Row {row_num}: {str(e)}")
                
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            self.import_stats['errors'].append(f"File error: {str(e)}")
        
        return self.import_stats
    
    def import_police_stations_csv(self, file_path: str) -> Dict[str, Any]:
        """Import Police Stations from CSV file"""
        self.import_stats = {'successful': 0, 'failed': 0, 'skipped': 0, 'errors': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Map CSV columns to database fields
                        station_data = {
                            'name': row.get('name', '').strip(),
                            'address': row.get('address', '').strip(),
                            'phone': row.get('phone', '').strip(),
                            'location': row.get('location', '').strip(),
                            'station_code': row.get('station_code', '').strip(),
                            'is_24x7': row.get('is_24x7', 'true').lower() == 'true',
                            'jurisdiction': row.get('jurisdiction', '').strip(),
                            'officer_in_charge': row.get('officer_in_charge', '').strip()
                        }
                        
                        # Validate required fields
                        if not station_data['name']:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Missing station name")
                            continue
                        
                        # Create new police station
                        station = PoliceStation(**station_data)
                        db.session.add(station)
                        self.import_stats['successful'] += 1
                        
                    except Exception as e:
                        self.import_stats['failed'] += 1
                        self.import_stats['errors'].append(f"Row {row_num}: {str(e)}")
                
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            self.import_stats['errors'].append(f"File error: {str(e)}")
        
        return self.import_stats
    
    def import_blood_banks_csv(self, file_path: str) -> Dict[str, Any]:
        """Import Blood Banks from CSV file"""
        self.import_stats = {'successful': 0, 'failed': 0, 'skipped': 0, 'errors': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Map CSV columns to database fields
                        bank_data = {
                            'name': row.get('name', '').strip(),
                            'address': row.get('address', '').strip(),
                            'phone': row.get('phone', '').strip(),
                            'location': row.get('location', '').strip(),
                            'is_24x7': row.get('is_24x7', 'false').lower() == 'true',
                            'blood_types_available': row.get('blood_types_available', '').strip(),
                            'contact_person': row.get('contact_person', '').strip(),
                            'license_number': row.get('license_number', '').strip()
                        }
                        
                        # Validate required fields
                        if not bank_data['name']:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Missing bank name")
                            continue
                        
                        # Create new blood bank
                        bank = BloodBank(**bank_data)
                        db.session.add(bank)
                        self.import_stats['successful'] += 1
                        
                    except Exception as e:
                        self.import_stats['failed'] += 1
                        self.import_stats['errors'].append(f"Row {row_num}: {str(e)}")
                
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            self.import_stats['errors'].append(f"File error: {str(e)}")
        
        return self.import_stats
    
    def import_fire_stations_csv(self, file_path: str) -> Dict[str, Any]:
        """Import Fire Stations from CSV file"""
        self.import_stats = {'successful': 0, 'failed': 0, 'skipped': 0, 'errors': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Map CSV columns to database fields
                        station_data = {
                            'name': row.get('name', '').strip(),
                            'address': row.get('address', '').strip(),
                            'phone': row.get('phone', '').strip(),
                            'location': row.get('location', '').strip(),
                            'station_code': row.get('station_code', '').strip(),
                            'is_24x7': row.get('is_24x7', 'true').lower() == 'true',
                            'equipment_available': row.get('equipment_available', '').strip(),
                            'chief_officer': row.get('chief_officer', '').strip()
                        }
                        
                        # Validate required fields
                        if not station_data['name']:
                            self.import_stats['skipped'] += 1
                            self.import_stats['errors'].append(f"Row {row_num}: Missing station name")
                            continue
                        
                        # Create new fire station
                        station = FireStation(**station_data)
                        db.session.add(station)
                        self.import_stats['successful'] += 1
                        
                    except Exception as e:
                        self.import_stats['failed'] += 1
                        self.import_stats['errors'].append(f"Row {row_num}: {str(e)}")
                
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            self.import_stats['errors'].append(f"File error: {str(e)}")
        
        return self.import_stats


class DataExporter:
    """Handles exporting data to various formats"""
    
    @staticmethod
    def export_ngos_to_csv(file_path: str) -> bool:
        """Export NGOs to CSV file"""
        try:
            ngos = NGO.query.all()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'name', 'email', 'phone', 'location', 'operating_zones', 'approved', 'created_at']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for ngo in ngos:
                    writer.writerow({
                        'id': ngo.id,
                        'name': ngo.name,
                        'email': ngo.email,
                        'phone': ngo.phone,
                        'location': ngo.location,
                        'operating_zones': ngo.operating_zones,
                        'approved': ngo.approved,
                        'created_at': ngo.created_at.isoformat() if ngo.created_at else ''
                    })
            
            return True
            
        except Exception as e:
            print(f"Export error: {str(e)}")
            return False
    
    @staticmethod
    def export_volunteers_to_csv(file_path: str) -> bool:
        """Export Volunteers to CSV file"""
        try:
            volunteers = Volunteer.query.all()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'name', 'email', 'phone', 'location', 'expertise', 'availability', 'approved', 'ngo_id', 'created_at']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for volunteer in volunteers:
                    writer.writerow({
                        'id': volunteer.id,
                        'name': volunteer.name,
                        'email': volunteer.email,
                        'phone': volunteer.phone,
                        'location': volunteer.location,
                        'expertise': volunteer.expertise,
                        'availability': volunteer.availability,
                        'approved': volunteer.approved,
                        'ngo_id': volunteer.ngo_id,
                        'created_at': volunteer.created_at.isoformat() if volunteer.created_at else ''
                    })
            
            return True
            
        except Exception as e:
            print(f"Export error: {str(e)}")
            return False


class DataAnalyzer:
    """Analyzes imported data for insights and statistics"""
    
    @staticmethod
    def get_import_statistics() -> Dict[str, Any]:
        """Get overall statistics about imported data"""
        stats = {
            'ngos': {
                'total': NGO.query.count(),
                'approved': NGO.query.filter_by(approved=True).count(),
                'pending': NGO.query.filter_by(approved=False).count()
            },
            'volunteers': {
                'total': Volunteer.query.count(),
                'approved': Volunteer.query.filter_by(approved=True).count(),
                'pending': Volunteer.query.filter_by(approved=False).count()
            },
            'hospitals': {
                'total': Hospital.query.count(),
                '24x7': Hospital.query.filter_by(is_24x7=True).count()
            },
            'police_stations': {
                'total': PoliceStation.query.count(),
                '24x7': PoliceStation.query.filter_by(is_24x7=True).count()
            },
            'blood_banks': {
                'total': BloodBank.query.count(),
                '24x7': BloodBank.query.filter_by(is_24x7=True).count()
            },
            'fire_stations': {
                'total': FireStation.query.count(),
                '24x7': FireStation.query.filter_by(is_24x7=True).count()
            },
            'emergency_contacts': {
                'total': EmergencyContact.query.count(),
                'by_service_type': {}
            }
        }
        
        # Get emergency contacts by service type
        contacts_by_type = db.session.query(
            EmergencyContact.service_type, 
            db.func.count(EmergencyContact.id)
        ).group_by(EmergencyContact.service_type).all()
        
        stats['emergency_contacts']['by_service_type'] = {
            service_type: count for service_type, count in contacts_by_type
        }
        
        return stats
    
    @staticmethod
    def get_location_distribution() -> Dict[str, Any]:
        """Get distribution of entities by location"""
        locations = {}
        
        # Count NGOs by location
        ngos_by_location = db.session.query(NGO.location, db.func.count(NGO.id)).group_by(NGO.location).all()
        locations['ngos'] = {location: count for location, count in ngos_by_location if location}
        
        # Count Volunteers by location
        volunteers_by_location = db.session.query(Volunteer.location, db.func.count(Volunteer.id)).group_by(Volunteer.location).all()
        locations['volunteers'] = {location: count for location, count in volunteers_by_location if location}
        
        # Count Hospitals by location
        hospitals_by_location = db.session.query(Hospital.location, db.func.count(Hospital.id)).group_by(Hospital.location).all()
        locations['hospitals'] = {location: count for location, count in hospitals_by_location if location}
        
        # Count Police Stations by location
        police_by_location = db.session.query(PoliceStation.location, db.func.count(PoliceStation.id)).group_by(PoliceStation.location).all()
        locations['police_stations'] = {location: count for location, count in police_by_location if location}
        
        # Count Blood Banks by location
        blood_banks_by_location = db.session.query(BloodBank.location, db.func.count(BloodBank.id)).group_by(BloodBank.location).all()
        locations['blood_banks'] = {location: count for location, count in blood_banks_by_location if location}
        
        # Count Fire Stations by location
        fire_stations_by_location = db.session.query(FireStation.location, db.func.count(FireStation.id)).group_by(FireStation.location).all()
        locations['fire_stations'] = {location: count for location, count in fire_stations_by_location if location}
        
        return locations