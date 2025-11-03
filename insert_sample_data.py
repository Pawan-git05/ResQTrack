#!/usr/bin/env python3
"""
Script to insert sample data into ResQTrack database
This script will populate the database with sample data for hospitals, NGOs, reports (animal cases), and volunteers.
"""

import os
import sys
from datetime import datetime
from decimal import Decimal

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from app.models import db, NGO, Volunteer, Hospital, AnimalCase, Donation, Admin
from app.extensions import bcrypt


def insert_sample_data():
    """Insert sample data into the database"""
    
    # Create Flask app and database context
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        print("Inserting sample data into ResQTrack database...")
        
        # 1. Insert Admins
        print("Inserting admins...")
        admin_data = [
            {
                'name': 'Super Admin',
                'email': 'admin@resqtrack.com',
                'password': 'admin123',
                'is_superadmin': True
            },
            {
                'name': 'John Doe',
                'email': 'john@resqtrack.com',
                'password': 'john123',
                'is_superadmin': False
            }
        ]
        
        for admin_info in admin_data:
            existing_admin = Admin.query.filter_by(email=admin_info['email']).first()
            if not existing_admin:
                admin = Admin(
                    name=admin_info['name'],
                    email=admin_info['email'],
                    password_hash=bcrypt.generate_password_hash(admin_info['password']).decode('utf-8'),
                    is_superadmin=admin_info['is_superadmin']
                )
                db.session.add(admin)
                print(f"  - Added admin: {admin_info['name']}")
        
        # 2. Insert NGOs
        print("Inserting NGOs...")
        ngo_data = [
            {
                'name': 'Paws Care Foundation',
                'email': 'contact@pawscare.org',
                'phone': '9999999999',
                'location': 'City Center',
                'operating_zones': 'Sector 1, Sector 2, Sector 3',
                'approved': True
            },
            {
                'name': 'Animal Rescue Society',
                'email': 'info@animalrescue.org',
                'phone': '8888888888',
                'location': 'Suburb Area',
                'operating_zones': 'Sector 4, Sector 5',
                'approved': True
            },
            {
                'name': 'Street Animals Help',
                'email': 'help@streetanimals.org',
                'phone': '7777777777',
                'location': 'Downtown',
                'operating_zones': 'Sector 6, Sector 7',
                'approved': False
            },
            {
                'name': 'Wildlife Protection NGO',
                'email': 'wildlife@protection.org',
                'phone': '6666666666',
                'location': 'Forest Area',
                'operating_zones': 'Rural Areas, Forest Zones',
                'approved': True
            }
        ]
        
        ngo_ids = []
        for ngo_info in ngo_data:
            existing_ngo = NGO.query.filter_by(email=ngo_info['email']).first()
            if not existing_ngo:
                ngo = NGO(**ngo_info)
                db.session.add(ngo)
                db.session.flush()  # Get the ID
                ngo_ids.append(ngo.id)
                print(f"  - Added NGO: {ngo_info['name']}")
            else:
                ngo_ids.append(existing_ngo.id)
        
        # 3. Insert Volunteers
        print("Inserting volunteers...")
        volunteer_data = [
            {
                'name': 'Riya Sharma',
                'email': 'riya@example.com',
                'phone': '8888888888',
                'location': 'Sector 1',
                'expertise': 'Pickup, First Aid',
                'availability': 'Evenings, Weekends',
                'approved': True,
                'ngo_id': ngo_ids[0] if ngo_ids else None
            },
            {
                'name': 'Amit Kumar',
                'email': 'amit@example.com',
                'phone': '7777777777',
                'location': 'Sector 2',
                'expertise': 'Transportation',
                'availability': 'Mornings, Afternoons',
                'approved': True,
                'ngo_id': ngo_ids[0] if ngo_ids else None
            },
            {
                'name': 'Priya Singh',
                'email': 'priya@example.com',
                'phone': '6666666666',
                'location': 'Sector 4',
                'expertise': 'Foster Care',
                'availability': 'Flexible',
                'approved': True,
                'ngo_id': ngo_ids[1] if len(ngo_ids) > 1 else None
            },
            {
                'name': 'Raj Patel',
                'email': 'raj@example.com',
                'phone': '5555555555',
                'location': 'Sector 5',
                'expertise': 'Emergency Response',
                'availability': '24/7',
                'approved': True,
                'ngo_id': ngo_ids[1] if len(ngo_ids) > 1 else None
            },
            {
                'name': 'Sneha Gupta',
                'email': 'sneha@example.com',
                'phone': '4444444444',
                'location': 'Sector 6',
                'expertise': 'Medical Care',
                'availability': 'Weekdays',
                'approved': False,
                'ngo_id': ngo_ids[2] if len(ngo_ids) > 2 else None
            }
        ]
        
        volunteer_ids = []
        for volunteer_info in volunteer_data:
            existing_volunteer = Volunteer.query.filter_by(email=volunteer_info['email']).first()
            if not existing_volunteer:
                volunteer = Volunteer(**volunteer_info)
                db.session.add(volunteer)
                db.session.flush()  # Get the ID
                volunteer_ids.append(volunteer.id)
                print(f"  - Added volunteer: {volunteer_info['name']}")
            else:
                volunteer_ids.append(existing_volunteer.id)
        
        # 4. Insert Hospitals
        print("Inserting hospitals...")
        hospital_data = [
            {
                'name': 'City Veterinary Clinic',
                'address': '123 Main Road, City Center',
                'phone': '9999999999',
                'location': 'Sector 15',
                'is_24x7': True,
                'treatment_types': 'Surgery, First Aid, Emergency Care'
            },
            {
                'name': 'Animal Care Hospital',
                'address': '456 Park Avenue, Suburb',
                'phone': '8888888888',
                'location': 'Sector 20',
                'is_24x7': False,
                'treatment_types': 'General Treatment, Vaccination'
            },
            {
                'name': 'Emergency Pet Clinic',
                'address': '789 Emergency Lane, Downtown',
                'phone': '7777777777',
                'location': 'Sector 25',
                'is_24x7': True,
                'treatment_types': 'Emergency Surgery, Critical Care'
            },
            {
                'name': 'Wildlife Rehabilitation Center',
                'address': '321 Forest Road, Rural Area',
                'phone': '6666666666',
                'location': 'Forest Zone',
                'is_24x7': False,
                'treatment_types': 'Wildlife Care, Rehabilitation'
            }
        ]
        
        hospital_ids = []
        for hospital_info in hospital_data:
            existing_hospital = Hospital.query.filter_by(name=hospital_info['name']).first()
            if not existing_hospital:
                hospital = Hospital(**hospital_info)
                db.session.add(hospital)
                db.session.flush()  # Get the ID
                hospital_ids.append(hospital.id)
                print(f"  - Added hospital: {hospital_info['name']}")
            else:
                hospital_ids.append(existing_hospital.id)
        
        # 5. Insert Animal Cases (Reports)
        print("Inserting animal cases (reports)...")
        case_data = [
            {
                'case_code': 'A250101120000123',
                'reporter_name': 'Amit Kumar',
                'reporter_phone': '9000000000',
                'location': 'Sector 15, Near Park',
                'latitude': 28.6139,
                'longitude': 77.2090,
                'animal_type': 'Dog',
                'urgency': 'Medium',
                'notes': 'Injured dog found near the park. Seems to have a leg injury.',
                'status': 'PENDING',
                'ngo_id': ngo_ids[0] if ngo_ids else None,
                'assigned_volunteer_id': volunteer_ids[0] if volunteer_ids else None,
                'hospital_id': hospital_ids[0] if hospital_ids else None
            },
            {
                'case_code': 'A250101120000124',
                'reporter_name': 'Priya Singh',
                'reporter_phone': '8000000000',
                'location': 'Sector 20, Street Corner',
                'latitude': 28.6140,
                'longitude': 77.2091,
                'animal_type': 'Cat',
                'urgency': 'Critical',
                'notes': 'Cat stuck in drain pipe. Needs immediate rescue.',
                'status': 'IN_PROGRESS',
                'ngo_id': ngo_ids[1] if len(ngo_ids) > 1 else None,
                'assigned_volunteer_id': volunteer_ids[1] if len(volunteer_ids) > 1 else None,
                'hospital_id': hospital_ids[1] if len(hospital_ids) > 1 else None
            },
            {
                'case_code': 'A250101120000125',
                'reporter_name': 'Raj Patel',
                'reporter_phone': '7000000000',
                'location': 'Sector 25, Construction Site',
                'latitude': 28.6141,
                'longitude': 77.2092,
                'animal_type': 'Bird',
                'urgency': 'Low',
                'notes': 'Bird with broken wing found at construction site.',
                'status': 'RESCUED',
                'ngo_id': ngo_ids[0] if ngo_ids else None,
                'assigned_volunteer_id': volunteer_ids[2] if len(volunteer_ids) > 2 else None,
                'hospital_id': hospital_ids[2] if len(hospital_ids) > 2 else None
            },
            {
                'case_code': 'A250101120000126',
                'reporter_name': 'Sneha Gupta',
                'reporter_phone': '6000000000',
                'location': 'Forest Area, Near Highway',
                'latitude': 28.6142,
                'longitude': 77.2093,
                'animal_type': 'Other',
                'urgency': 'Medium',
                'notes': 'Deer found injured near highway. Wildlife rescue needed.',
                'status': 'PENDING',
                'ngo_id': ngo_ids[3] if len(ngo_ids) > 3 else None,
                'assigned_volunteer_id': volunteer_ids[3] if len(volunteer_ids) > 3 else None,
                'hospital_id': hospital_ids[3] if len(hospital_ids) > 3 else None
            },
            {
                'case_code': 'A250101120000127',
                'reporter_name': 'Anonymous',
                'reporter_phone': '5000000000',
                'location': 'Sector 10, Residential Area',
                'latitude': 28.6143,
                'longitude': 77.2094,
                'animal_type': 'Dog',
                'urgency': 'Critical',
                'notes': 'Dog hit by vehicle. Bleeding heavily. Emergency required.',
                'status': 'IN_PROGRESS',
                'ngo_id': ngo_ids[0] if ngo_ids else None,
                'assigned_volunteer_id': volunteer_ids[4] if len(volunteer_ids) > 4 else None,
                'hospital_id': hospital_ids[0] if hospital_ids else None
            }
        ]
        
        for case_info in case_data:
            existing_case = AnimalCase.query.filter_by(case_code=case_info['case_code']).first()
            if not existing_case:
                case = AnimalCase(**case_info)
                db.session.add(case)
                print(f"  - Added case: {case_info['case_code']}")
        
        # 6. Insert Donations
        print("Inserting donations...")
        donation_data = [
            {
                'donor_name': 'Neha Sharma',
                'donor_email': 'neha@example.com',
                'amount': Decimal('500.00'),
                'currency': 'INR',
                'category': 'Medical Aid',
                'payment_provider': 'Razorpay',
                'payment_id': 'pay_123456789',
                'ngo_id': ngo_ids[0] if ngo_ids else None
            },
            {
                'donor_name': 'Vikram Singh',
                'donor_email': 'vikram@example.com',
                'amount': Decimal('1000.00'),
                'currency': 'INR',
                'category': 'Food Supplies',
                'payment_provider': 'Razorpay',
                'payment_id': 'pay_123456790',
                'ngo_id': ngo_ids[1] if len(ngo_ids) > 1 else None
            },
            {
                'donor_name': 'Anita Patel',
                'donor_email': 'anita@example.com',
                'amount': Decimal('2500.00'),
                'currency': 'INR',
                'category': 'Shelter',
                'payment_provider': 'Razorpay',
                'payment_id': 'pay_123456791',
                'ngo_id': ngo_ids[0] if ngo_ids else None
            },
            {
                'donor_name': 'Rohit Kumar',
                'donor_email': 'rohit@example.com',
                'amount': Decimal('750.00'),
                'currency': 'INR',
                'category': 'Emergency Fund',
                'payment_provider': 'Razorpay',
                'payment_id': 'pay_123456792',
                'ngo_id': ngo_ids[3] if len(ngo_ids) > 3 else None
            },
            {
                'donor_name': 'Anonymous',
                'donor_email': None,
                'amount': Decimal('200.00'),
                'currency': 'INR',
                'category': 'General',
                'payment_provider': 'Razorpay',
                'payment_id': 'pay_123456793',
                'ngo_id': ngo_ids[2] if len(ngo_ids) > 2 else None
            }
        ]
        
        for donation_info in donation_data:
            existing_donation = Donation.query.filter_by(payment_id=donation_info['payment_id']).first()
            if not existing_donation:
                donation = Donation(**donation_info)
                db.session.add(donation)
                print(f"  - Added donation: {donation_info['amount']} {donation_info['currency']} from {donation_info['donor_name'] or 'Anonymous'}")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Sample data inserted successfully!")
        print(f"📊 Summary:")
        print(f"   - Admins: {len(admin_data)}")
        print(f"   - NGOs: {len(ngo_data)}")
        print(f"   - Volunteers: {len(volunteer_data)}")
        print(f"   - Hospitals: {len(hospital_data)}")
        print(f"   - Animal Cases: {len(case_data)}")
        print(f"   - Donations: {len(donation_data)}")


if __name__ == "__main__":
    try:
        insert_sample_data()
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        sys.exit(1)
