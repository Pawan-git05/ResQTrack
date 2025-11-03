"""
Frontend integration tests to verify all buttons and features work.
Run with: pytest tests/test_frontend_integration.py -v
"""
import pytest
from backend.app.extensions import db
from backend.app.models import Admin, Hospital, PoliceStation
from backend.app.utils import hash_password


def test_report_case_endpoint(client):
    """Test case reporting endpoint (used by Report button)"""
    response = client.post('/cases', json={
        'reporter_phone': '9999999999',
        'location': 'Test City',
        'animal_type': 'Dog',
        'urgency': 'Low',
        'notes': 'Test case'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'case_id' in data
    assert 'case_code' in data


def test_register_ngo_endpoint(client):
    """Test NGO registration endpoint (used by Register page)"""
    response = client.post('/register/ngo', json={
        'name': 'Test NGO',
        'email': 'test@ngo.com',
        'phone': '1234567890',
        'location': 'Test City'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'ngo_id' in data


def test_register_volunteer_endpoint(client):
    """Test volunteer registration endpoint (used by Register page)"""
    response = client.post('/register/volunteer', json={
        'name': 'Test Volunteer',
        'email': 'test@volunteer.com',
        'phone': '9876543210',
        'location': 'Test City'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'volunteer_id' in data


def test_donate_endpoint(client):
    """Test donation endpoint (used by Donate button)"""
    response = client.post('/donations', json={
        'donor_name': 'Test Donor',
        'donor_email': 'donor@test.com',
        'amount': 500,
        'currency': 'INR',
        'category': 'General'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data


def test_list_hospitals_endpoint(client):
    """Test hospitals listing endpoint (used by Hospitals page)"""
    # Add test hospital
    hospital = Hospital(
        name="Test Hospital",
        address="123 Test St",
        phone="1234567890"
    )
    db.session.add(hospital)
    db.session.commit()

    response = client.get('/hospitals')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) > 0


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_duplicate_ngo_registration(client):
    """Test that duplicate NGO email is rejected"""
    payload = {
        'name': 'Duplicate NGO',
        'email': 'duplicate@ngo.com',
        'phone': '1234567890'
    }
    
    # First registration
    response1 = client.post('/register/ngo', json=payload)
    assert response1.status_code == 201
    
    # Duplicate registration
    response2 = client.post('/register/ngo', json=payload)
    assert response2.status_code == 409


def test_duplicate_volunteer_registration(client):
    """Test that duplicate volunteer email is rejected"""
    payload = {
        'name': 'Duplicate Volunteer',
        'email': 'duplicate@vol.com',
        'phone': '1234567890'
    }
    
    # First registration
    response1 = client.post('/register/volunteer', json=payload)
    assert response1.status_code == 201
    
    # Duplicate registration
    response2 = client.post('/register/volunteer', json=payload)
    assert response2.status_code == 409


def test_case_with_missing_fields(client):
    """Test case creation with missing required fields"""
    response = client.post('/cases', json={
        'location': 'Test City'
        # Missing reporter_phone
    })
    assert response.status_code == 400


def test_ngo_registration_missing_fields(client):
    """Test NGO registration with missing fields"""
    response = client.post('/register/ngo', json={
        'name': 'Incomplete NGO'
        # Missing email and phone
    })
    assert response.status_code == 400


def test_volunteer_registration_missing_fields(client):
    """Test volunteer registration with missing fields"""
    response = client.post('/register/volunteer', json={
        'name': 'Incomplete Volunteer'
        # Missing email and phone
    })
    assert response.status_code == 400
