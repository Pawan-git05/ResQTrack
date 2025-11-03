#!/usr/bin/env python
"""
Seed admin user and sample data for testing.
Run this before testing the admin dashboard.
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import Admin, AnimalCase, NGO, Volunteer, Donation, Hospital, AnimalType
from backend.app.utils import hash_password


def seed_database():
    """Seed database with admin user and sample data"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Seeding database...")
        
        # Create admin user
        existing_admin = Admin.query.filter_by(email='admin@resqtrack.com').first()
        if not existing_admin:
            admin = Admin(
                email='admin@resqtrack.com',
                name='Admin User',
                password_hash=hash_password('admin123')
            )
            db.session.add(admin)
            print("✅ Created admin user (email: admin@resqtrack.com, password: admin123)")
        else:
            print("ℹ️  Admin user already exists")
        
        # Create sample cases
        if AnimalCase.query.count() == 0:
            cases = [
                AnimalCase(
                    reporter_name="John Doe",
                    reporter_phone="9876543210",
                    location="MG Road, Bangalore",
                    animal_type=AnimalType.DOG,
                    urgency="High",
                    notes="Injured dog on roadside",
                    case_code="CASE001"
                ),
                AnimalCase(
                    reporter_name="Jane Smith",
                    reporter_phone="8765432109",
                    location="Koramangala, Bangalore",
                    animal_type=AnimalType.CAT,
                    urgency="Medium",
                    notes="Stray cat needs food",
                    case_code="CASE002"
                ),
                AnimalCase(
                    reporter_phone="7654321098",
                    location="Indiranagar, Bangalore",
                    animal_type=AnimalType.OTHER,
                    urgency="Low",
                    notes="Cow blocking traffic",
                    case_code="CASE003"
                )
            ]
            for case in cases:
                db.session.add(case)
            print(f"✅ Created {len(cases)} sample cases")
        
        # Create sample NGOs
        if NGO.query.count() == 0:
            ngos = [
                NGO(
                    name="Animal Rescue Foundation",
                    email="arf@rescue.org",
                    phone="9999999991",
                    location="Bangalore",
                    operating_zones="Bangalore, Mysore",
                    approved=True
                ),
                NGO(
                    name="Wildlife Protection Society",
                    email="wps@wildlife.org",
                    phone="9999999992",
                    location="Mumbai",
                    operating_zones="Mumbai, Pune",
                    approved=False
                )
            ]
            for ngo in ngos:
                db.session.add(ngo)
            print(f"✅ Created {len(ngos)} sample NGOs")
        
        # Create sample volunteers
        if Volunteer.query.count() == 0:
            volunteers = [
                Volunteer(
                    name="Alice Johnson",
                    email="alice@volunteer.com",
                    phone="8888888881",
                    location="Bangalore",
                    expertise="First Aid",
                    approved=True
                ),
                Volunteer(
                    name="Bob Williams",
                    email="bob@volunteer.com",
                    phone="8888888882",
                    location="Delhi",
                    expertise="Transport",
                    approved=False
                )
            ]
            for vol in volunteers:
                db.session.add(vol)
            print(f"✅ Created {len(volunteers)} sample volunteers")
        
        # Create sample donations
        if Donation.query.count() == 0:
            donations = [
                Donation(
                    donor_name="Rajesh Kumar",
                    donor_email="rajesh@donor.com",
                    amount=5000.0,
                    currency="INR",
                    category="Medical",
                    payment_provider="Razorpay"
                ),
                Donation(
                    donor_name="Priya Sharma",
                    donor_email="priya@donor.com",
                    amount=2000.0,
                    currency="INR",
                    category="Food",
                    payment_provider="Stripe"
                )
            ]
            for donation in donations:
                db.session.add(donation)
            print(f"✅ Created {len(donations)} sample donations")
        
        # Create sample hospitals
        if Hospital.query.count() == 0:
            hospitals = [
                Hospital(
                    name="City Veterinary Hospital",
                    address="123 Main Street, Bangalore",
                    phone="080-12345678",
                    location="Bangalore",
                    is_24x7=True,
                    treatment_types="Emergency, Surgery, General Care"
                ),
                Hospital(
                    name="Animal Care Clinic",
                    address="456 Park Avenue, Mumbai",
                    phone="022-87654321",
                    location="Mumbai",
                    is_24x7=False,
                    treatment_types="Vaccination, Checkup"
                )
            ]
            for hospital in hospitals:
                db.session.add(hospital)
            print(f"✅ Created {len(hospitals)} sample hospitals")
        
        db.session.commit()
        print("\n🎉 Database seeded successfully!")
        print("\n📋 Admin Credentials:")
        print("   Email: admin@resqtrack.com")
        print("   Password: admin123")
        print("\n🌐 Access admin dashboard at: http://localhost:8000/admin.html")


if __name__ == "__main__":
    seed_database()
