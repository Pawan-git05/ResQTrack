"""
End-to-end tests for admin dashboard functionality.
Tests all buttons, CRUD operations, and UI interactions.
"""
import pytest
from backend.app.extensions import db
from backend.app.models import (
    Admin, AnimalCase, NGO, Volunteer, Donation, Hospital,
    PoliceStation, BloodBank, FireStation, EmergencyContact, CaseStatus
)
from backend.app.utils import hash_password


@pytest.fixture
def seed_admin(app):
    """Create admin user for testing"""
    with app.app_context():
        admin = Admin(
            email="admin@resqtrack.com",
            name="Test Admin",
            password_hash=hash_password("admin123")
        )
        db.session.add(admin)
        db.session.commit()
        return admin


@pytest.fixture
def admin_token(client, seed_admin):
    """Get admin JWT token"""
    response = client.post('/auth/login', json={
        'email': 'admin@resqtrack.com',
        'password': 'admin123',
        'role': 'ADMIN'
    })
    assert response.status_code == 200
    return response.get_json()['access_token']


def test_admin_login(client, seed_admin):
    """Test admin can login"""
    response = client.post('/auth/login', json={
        'email': 'admin@resqtrack.com',
        'password': 'admin123',
        'role': 'ADMIN'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_get_all_cases(client, admin_token):
    """Test fetching all cases"""
    # Create test case
    case = AnimalCase(
        reporter_phone="9999999999",
        location="Test Location",
        animal_type="Dog",
        urgency="Low",
        case_code="TEST001"
    )
    db.session.add(case)
    db.session.commit()

    response = client.get('/admin/cases', headers={
        'Authorization': f'Bearer {admin_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'cases' in data
    assert len(data['cases']) > 0


def test_get_all_ngos(client, admin_token):
    """Test fetching all NGOs"""
    ngo = NGO(
        name="Test NGO",
        email="ngo@test.com",
        phone="1234567890"
    )
    db.session.add(ngo)
    db.session.commit()

    response = client.get('/admin/ngos', headers={
        'Authorization': f'Bearer {admin_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'ngos' in data
    assert len(data['ngos']) > 0


def test_get_all_volunteers(client, admin_token):
    """Test fetching all volunteers"""
    vol = Volunteer(
        name="Test Volunteer",
        email="vol@test.com",
        phone="1234567890"
    )
    db.session.add(vol)
    db.session.commit()

    response = client.get('/admin/volunteers', headers={
        'Authorization': f'Bearer {admin_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'volunteers' in data
    assert len(data['volunteers']) > 0


def test_get_all_donations(client, admin_token):
    """Test fetching all donations"""
    donation = Donation(
        donor_name="Test Donor",
        amount=100.0,
        currency="INR",
        category="General"
    )
    db.session.add(donation)
    db.session.commit()

    response = client.get('/admin/donations', headers={
        'Authorization': f'Bearer {admin_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'donations' in data
    assert len(data['donations']) > 0


def test_get_all_hospitals(client, admin_token):
    """Test fetching all hospitals"""
    hospital = Hospital(
        name="Test Hospital",
        address="123 Test St",
        phone="1234567890"
    )
    db.session.add(hospital)
    db.session.commit()

    response = client.get('/admin/hospitals', headers={
        'Authorization': f'Bearer {admin_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'hospitals' in data
    assert len(data['hospitals']) > 0


def test_add_hospital(client, admin_token):
    """Test adding a new hospital"""
    response = client.post('/admin/hospitals', 
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'New Hospital',
            'address': '456 New St',
            'phone': '9876543210',
            'is_24x7': True,
            'treatment_types': 'Emergency, Surgery'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['message'] == 'Hospital added successfully'


def test_add_police_station(client, admin_token):
    """Test adding a new police station"""
    response = client.post('/admin/police-stations',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Test Police Station',
            'address': '789 Police St',
            'phone': '100',
            'station_code': 'PS001',
            'jurisdiction': 'Test Area',
            'officer_in_charge': 'Officer Test'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data


def test_add_blood_bank(client, admin_token):
    """Test adding a new blood bank"""
    response = client.post('/admin/blood-banks',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Test Blood Bank',
            'address': '321 Blood St',
            'phone': '1122334455',
            'blood_types_available': 'A+, B+, O+',
            'contact_person': 'Dr. Test',
            'license_number': 'BB12345'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data


def test_add_fire_station(client, admin_token):
    """Test adding a new fire station"""
    response = client.post('/admin/fire-stations',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Test Fire Station',
            'address': '555 Fire St',
            'phone': '101',
            'station_code': 'FS001',
            'equipment_available': 'Fire trucks, Ladder',
            'chief_officer': 'Chief Test'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data


def test_add_emergency_contact(client, admin_token):
    """Test adding a new emergency contact"""
    response = client.post('/admin/emergency-contacts',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Test Emergency Contact',
            'phone': '112',
            'email': 'emergency@test.com',
            'service_type': 'Medical',
            'location': 'Test City',
            'priority_level': 1
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data


def test_approve_ngo(client, admin_token):
    """Test approving an NGO"""
    ngo = NGO(
        name="Pending NGO",
        email="pending@ngo.com",
        phone="1234567890",
        approved=False
    )
    db.session.add(ngo)
    db.session.commit()

    response = client.patch(f'/admin/ngos/{ngo.id}/approve',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    
    # Verify approval
    updated_ngo = NGO.query.get(ngo.id)
    assert updated_ngo.approved is True


def test_approve_volunteer(client, admin_token):
    """Test approving a volunteer"""
    vol = Volunteer(
        name="Pending Volunteer",
        email="pending@vol.com",
        phone="1234567890",
        approved=False
    )
    db.session.add(vol)
    db.session.commit()

    response = client.patch(f'/admin/volunteers/{vol.id}/approve',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    
    # Verify approval
    updated_vol = Volunteer.query.get(vol.id)
    assert updated_vol.approved is True


def test_update_case_status(client, admin_token):
    """Test updating case status"""
    case = AnimalCase(
        reporter_phone="9999999999",
        location="Test Location",
        animal_type="Dog",
        urgency="Low",
        case_code="STATUS001",
        status=CaseStatus.PENDING
    )
    db.session.add(case)
    db.session.commit()

    response = client.patch(f'/admin/cases/{case.id}/status',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'status': 'IN_PROGRESS'}
    )
    assert response.status_code == 200
    
    # Verify status update
    updated_case = AnimalCase.query.get(case.id)
    assert updated_case.status == CaseStatus.IN_PROGRESS


def test_csv_upload_hospitals(client, admin_token, tmp_path):
    """Test CSV upload for hospitals"""
    # Create a test CSV file
    csv_content = b"""name,address,phone,location,is_24x7,treatment_types
Test Hospital 1,123 Test St,1234567890,Test City,true,Emergency
Test Hospital 2,456 Test Ave,9876543210,Test Town,false,Surgery"""
    
    csv_file = tmp_path / "hospitals.csv"
    csv_file.write_bytes(csv_content)
    
    with open(csv_file, 'rb') as f:
        response = client.post('/admin/upload-csv/hospitals',
            headers={'Authorization': f'Bearer {admin_token}'},
            data={'file': (f, 'hospitals.csv')},
            content_type='multipart/form-data'
        )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['imported_count'] == 2


def test_unauthorized_access(client):
    """Test that endpoints require authentication"""
    endpoints = [
        '/admin/cases',
        '/admin/ngos',
        '/admin/volunteers',
        '/admin/donations',
        '/admin/hospitals',
        '/admin/police-stations',
        '/admin/blood-banks',
        '/admin/fire-stations',
        '/admin/emergency-contacts'
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401


def test_invalid_status_update(client, admin_token):
    """Test updating case with invalid status"""
    case = AnimalCase(
        reporter_phone="9999999999",
        location="Test Location",
        animal_type="Dog",
        urgency="Low",
        case_code="INVALID001"
    )
    db.session.add(case)
    db.session.commit()

    response = client.patch(f'/admin/cases/{case.id}/status',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'status': 'INVALID_STATUS'}
    )
    assert response.status_code == 400


def test_add_hospital_missing_name(client, admin_token):
    """Test adding hospital without required name field"""
    response = client.post('/admin/hospitals',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'address': '123 Test St',
            'phone': '1234567890'
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_get_police_stations(client, admin_token):
    """Test fetching all police stations"""
    station = PoliceStation(
        name="Test Station",
        phone="100",
        station_code="PS001"
    )
    db.session.add(station)
    db.session.commit()

    response = client.get('/admin/police-stations',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'police_stations' in data
    assert len(data['police_stations']) > 0


def test_get_blood_banks(client, admin_token):
    """Test fetching all blood banks"""
    bank = BloodBank(
        name="Test Blood Bank",
        phone="1234567890"
    )
    db.session.add(bank)
    db.session.commit()

    response = client.get('/admin/blood-banks',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'blood_banks' in data


def test_get_fire_stations(client, admin_token):
    """Test fetching all fire stations"""
    station = FireStation(
        name="Test Fire Station",
        phone="101"
    )
    db.session.add(station)
    db.session.commit()

    response = client.get('/admin/fire-stations',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'fire_stations' in data


def test_get_emergency_contacts(client, admin_token):
    """Test fetching all emergency contacts"""
    contact = EmergencyContact(
        name="Test Contact",
        phone="112",
        service_type="Medical"
    )
    db.session.add(contact)
    db.session.commit()

    response = client.get('/admin/emergency-contacts',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'emergency_contacts' in data
