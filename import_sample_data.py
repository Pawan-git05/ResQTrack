#!/usr/bin/env python3
"""
ResQTrack Data Import Script
Imports sample datasets into the ResQTrack database
"""

import os
import sys
import argparse
from pathlib import Path

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.app.extensions import db
from backend.app.data_integration import DatasetImporter
from backend.app.models import NGO, Volunteer, Hospital, PoliceStation, BloodBank, FireStation, EmergencyContact


def import_sample_data():
    """Import all sample datasets"""
    app = create_app()
    
    with app.app_context():
        importer = DatasetImporter()
        
        # Get the sample data directory
        sample_dir = Path(__file__).parent / 'sample_data'
        
        print("🚀 Starting ResQTrack Data Import...")
        print("=" * 50)
        
        # Import NGOs
        ngo_file = sample_dir / 'ngos.csv'
        if ngo_file.exists():
            print(f"📊 Importing NGOs from {ngo_file.name}...")
            result = importer.import_ngos_csv(str(ngo_file))
            print(f"   ✅ Successful: {result['successful']}")
            print(f"   ❌ Failed: {result['failed']}")
            print(f"   ⚠️  Skipped: {result['skipped']}")
            if result['errors']:
                print(f"   🔍 Errors: {len(result['errors'])}")
        else:
            print(f"⚠️  NGO file not found: {ngo_file}")
        
        print()
        
        # Import Volunteers
        volunteer_file = sample_dir / 'volunteers.csv'
        if volunteer_file.exists():
            print(f"👥 Importing Volunteers from {volunteer_file.name}...")
            result = importer.import_volunteers_csv(str(volunteer_file))
            print(f"   ✅ Successful: {result['successful']}")
            print(f"   ❌ Failed: {result['failed']}")
            print(f"   ⚠️  Skipped: {result['skipped']}")
            if result['errors']:
                print(f"   🔍 Errors: {len(result['errors'])}")
        else:
            print(f"⚠️  Volunteer file not found: {volunteer_file}")
        
        print()
        
        # Import Hospitals
        hospital_file = sample_dir / 'hospitals.csv'
        if hospital_file.exists():
            print(f"🏥 Importing Hospitals from {hospital_file.name}...")
            result = importer.import_hospitals_csv(str(hospital_file))
            print(f"   ✅ Successful: {result['successful']}")
            print(f"   ❌ Failed: {result['failed']}")
            print(f"   ⚠️  Skipped: {result['skipped']}")
            if result['errors']:
                print(f"   🔍 Errors: {len(result['errors'])}")
        else:
            print(f"⚠️  Hospital file not found: {hospital_file}")
        
        print()
        
        # Import Police Stations
        police_file = sample_dir / 'police_stations.csv'
        if police_file.exists():
            print(f"🚔 Importing Police Stations from {police_file.name}...")
            result = importer.import_police_stations_csv(str(police_file))
            print(f"   ✅ Successful: {result['successful']}")
            print(f"   ❌ Failed: {result['failed']}")
            print(f"   ⚠️  Skipped: {result['skipped']}")
            if result['errors']:
                print(f"   🔍 Errors: {len(result['errors'])}")
        else:
            print(f"⚠️  Police Station file not found: {police_file}")
        
        print()
        
        # Import Blood Banks
        blood_bank_file = sample_dir / 'blood_banks.csv'
        if blood_bank_file.exists():
            print(f"🩸 Importing Blood Banks from {blood_bank_file.name}...")
            result = importer.import_blood_banks_csv(str(blood_bank_file))
            print(f"   ✅ Successful: {result['successful']}")
            print(f"   ❌ Failed: {result['failed']}")
            print(f"   ⚠️  Skipped: {result['skipped']}")
            if result['errors']:
                print(f"   🔍 Errors: {len(result['errors'])}")
        else:
            print(f"⚠️  Blood Bank file not found: {blood_bank_file}")
        
        print()
        
        # Import Fire Stations
        fire_station_file = sample_dir / 'fire_stations.csv'
        if fire_station_file.exists():
            print(f"🚒 Importing Fire Stations from {fire_station_file.name}...")
            result = importer.import_fire_stations_csv(str(fire_station_file))
            print(f"   ✅ Successful: {result['successful']}")
            print(f"   ❌ Failed: {result['failed']}")
            print(f"   ⚠️  Skipped: {result['skipped']}")
            if result['errors']:
                print(f"   🔍 Errors: {len(result['errors'])}")
        else:
            print(f"⚠️  Fire Station file not found: {fire_station_file}")
        
        print()
        
        # Add some emergency contacts
        print("📞 Adding Emergency Contacts...")
        emergency_contacts = [
            {
                'name': 'National Emergency Number',
                'phone': '100',
                'service_type': 'Police',
                'location': 'All India',
                'is_24x7': True,
                'description': 'National police emergency number',
                'priority_level': 1
            },
            {
                'name': 'Fire Emergency Number',
                'phone': '101',
                'service_type': 'Fire',
                'location': 'All India',
                'is_24x7': True,
                'description': 'National fire emergency number',
                'priority_level': 1
            },
            {
                'name': 'Medical Emergency Number',
                'phone': '108',
                'service_type': 'Medical',
                'location': 'All India',
                'is_24x7': True,
                'description': 'National medical emergency number',
                'priority_level': 1
            },
            {
                'name': 'Disaster Management Helpline',
                'phone': '108',
                'service_type': 'Disaster',
                'location': 'All India',
                'is_24x7': True,
                'description': 'National disaster management helpline',
                'priority_level': 1
            }
        ]
        
        for contact_data in emergency_contacts:
            contact = EmergencyContact(**contact_data)
            db.session.add(contact)
        
        db.session.commit()
        print(f"   ✅ Added {len(emergency_contacts)} emergency contacts")
        
        print()
        print("=" * 50)
        print("🎉 Data import completed successfully!")
        print()
        
        # Show final statistics
        print("📊 Final Statistics:")
        print(f"   NGOs: {NGO.query.count()}")
        print(f"   Volunteers: {Volunteer.query.count()}")
        print(f"   Hospitals: {Hospital.query.count()}")
        print(f"   Police Stations: {PoliceStation.query.count()}")
        print(f"   Blood Banks: {BloodBank.query.count()}")
        print(f"   Fire Stations: {FireStation.query.count()}")
        print(f"   Emergency Contacts: {EmergencyContact.query.count()}")


def clear_all_data():
    """Clear all data from the database"""
    app = create_app()
    
    with app.app_context():
        print("🗑️  Clearing all data from ResQTrack database...")
        
        # Delete all records
        EmergencyContact.query.delete()
        FireStation.query.delete()
        BloodBank.query.delete()
        PoliceStation.query.delete()
        Hospital.query.delete()
        Volunteer.query.delete()
        NGO.query.delete()
        
        db.session.commit()
        print("✅ All data cleared successfully!")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='ResQTrack Data Import Tool')
    parser.add_argument('--clear', action='store_true', help='Clear all existing data before import')
    parser.add_argument('--import-only', action='store_true', help='Only import data, do not clear existing data')
    
    args = parser.parse_args()
    
    if args.clear:
        clear_all_data()
        print()
    
    if not args.clear or args.import_only:
        import_sample_data()


if __name__ == '__main__':
    main()
