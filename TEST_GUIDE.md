# ResQTrack Testing Guide

## Quick Start

### Run All Tests
```bash
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # macOS/Linux

# Run comprehensive test suite
python run_tests.py

# Or run with pytest directly
pytest -v
```

### Run Specific Test Suites

```bash
# Authentication tests
pytest tests/test_auth.py -v

# Case management tests
pytest tests/test_cases.py -v

# Upload functionality tests
pytest tests/test_uploads.py -v

# Admin dashboard tests (comprehensive)
pytest tests/test_e2e_admin.py -v

# Frontend integration tests
pytest tests/test_frontend_integration.py -v
```

## What Gets Tested

### ✅ Admin Dashboard (`test_e2e_admin.py`)
- **Login**: Admin authentication
- **View All Data**: Cases, NGOs, Volunteers, Donations, Hospitals, Police Stations, Blood Banks, Fire Stations, Emergency Contacts
- **Add New Records**: All entity types (hospitals, police stations, etc.)
- **Approve**: NGO and Volunteer approvals
- **Update**: Case status updates
- **CSV Upload**: Bulk data import for all services
- **Authorization**: Ensures endpoints require JWT
- **Error Handling**: Invalid inputs, missing fields

### ✅ Frontend Integration (`test_frontend_integration.py`)
- **Report Button**: Case creation endpoint
- **Register Page**: NGO and Volunteer registration
- **Donate Button**: Donation submission
- **Hospitals Page**: Hospital listing
- **Duplicate Prevention**: Email uniqueness validation
- **Required Fields**: Missing field validation

### ✅ Core Functionality
- **Auth**: Login flow, JWT tokens
- **Cases**: Public case creation, status updates
- **Uploads**: File upload with validation
- **Security**: Rate limiting, CORS, authentication

## Test Coverage

| Feature | Endpoint | Test Status |
|---------|----------|-------------|
| Admin Login | POST /auth/login | ✅ Tested |
| Get Cases | GET /admin/cases | ✅ Tested |
| Get NGOs | GET /admin/ngos | ✅ Tested |
| Get Volunteers | GET /admin/volunteers | ✅ Tested |
| Get Donations | GET /admin/donations | ✅ Tested |
| Get Hospitals | GET /admin/hospitals | ✅ Tested |
| Get Police Stations | GET /admin/police-stations | ✅ Tested |
| Get Blood Banks | GET /admin/blood-banks | ✅ Tested |
| Get Fire Stations | GET /admin/fire-stations | ✅ Tested |
| Get Emergency Contacts | GET /admin/emergency-contacts | ✅ Tested |
| Add Hospital | POST /admin/hospitals | ✅ Tested |
| Add Police Station | POST /admin/police-stations | ✅ Tested |
| Add Blood Bank | POST /admin/blood-banks | ✅ Tested |
| Add Fire Station | POST /admin/fire-stations | ✅ Tested |
| Add Emergency Contact | POST /admin/emergency-contacts | ✅ Tested |
| Approve NGO | PATCH /admin/ngos/:id/approve | ✅ Tested |
| Approve Volunteer | PATCH /admin/volunteers/:id/approve | ✅ Tested |
| Update Case Status | PATCH /admin/cases/:id/status | ✅ Tested |
| CSV Upload | POST /admin/upload-csv/:type | ✅ Tested |
| Report Case | POST /cases | ✅ Tested |
| Register NGO | POST /register/ngo | ✅ Tested |
| Register Volunteer | POST /register/volunteer | ✅ Tested |
| Donate | POST /donations | ✅ Tested |
| List Hospitals | GET /hospitals | ✅ Tested |
| Upload File | POST /uploads | ✅ Tested |

## Common Issues & Fixes

### Issue: Tests fail with "No module named 'backend'"
**Fix**: Ensure `pytest.ini` has `pythonpath = backend`

### Issue: Database errors
**Fix**: Tests use in-memory SQLite. Check `conftest.py` fixture setup.

### Issue: JWT authentication fails
**Fix**: Ensure admin user is seeded in `seed_admin` fixture.

### Issue: CSV upload tests fail
**Fix**: Check that test CSV files are properly formatted.

## Manual Testing Checklist

After running automated tests, manually verify:

### Admin Dashboard
- [ ] Login with admin@resqtrack.com / admin123
- [ ] All tabs load data (Cases, NGOs, Volunteers, etc.)
- [ ] Statistics cards show correct counts
- [ ] Add Hospital button opens modal
- [ ] Add Police Station button opens modal
- [ ] Map view switches work
- [ ] CSV import buttons work
- [ ] Refresh button reloads data
- [ ] Approve buttons work for NGOs/Volunteers
- [ ] Case status can be updated

### Frontend Pages
- [ ] Report page submits cases
- [ ] Register page submits NGO/Volunteer forms
- [ ] Donate page processes donations
- [ ] Hospitals page lists hospitals
- [ ] Toast notifications appear on success/error
- [ ] Loading spinners show during requests
- [ ] Form validation works

## Continuous Integration

Tests run automatically on push/PR via GitHub Actions:
- Python 3.11
- Linting with flake8
- Full test suite with pytest

See `.github/workflows/ci.yml` for configuration.

## Writing New Tests

### Example Test
```python
def test_new_feature(client, admin_token):
    """Test description"""
    response = client.post('/admin/new-endpoint',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'field': 'value'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
```

### Fixtures Available
- `app`: Flask app with test config
- `client`: Test client for making requests
- `admin_token`: JWT token for admin user
- `seed_admin`: Creates admin user in DB

## Performance Testing

For load testing admin dashboard:
```bash
# Install locust
pip install locust

# Create locustfile.py with admin scenarios
# Run: locust -f locustfile.py
```

## Debugging Failed Tests

```bash
# Run with verbose output
pytest tests/test_e2e_admin.py -vv

# Run specific test
pytest tests/test_e2e_admin.py::test_add_hospital -v

# Show print statements
pytest tests/test_e2e_admin.py -v -s

# Stop on first failure
pytest tests/test_e2e_admin.py -x
```

## Next Steps

1. Run `python run_tests.py` to verify all tests pass
2. Fix any failing tests
3. Start backend: `python backend/wsgi.py`
4. Start frontend: `cd frontend && python -m http.server 8000`
5. Manually test admin dashboard at http://localhost:8000/admin.html
6. Login with admin@resqtrack.com / admin123
7. Test all buttons and features

## Support

If tests fail or features don't work:
1. Check backend logs for errors
2. Check browser console for frontend errors
3. Verify database migrations are up to date: `flask db upgrade`
4. Ensure all dependencies are installed: `pip install -r requirements.txt`
