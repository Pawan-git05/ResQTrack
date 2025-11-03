# 🧪 ResQTrack - Complete Testing & Verification Guide

## 🚀 Quick Start (Test Everything in 5 Minutes)

### Step 1: Setup Environment
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Initialize Database
```powershell
set FLASK_APP=backend/wsgi.py
flask db upgrade
python seed_admin.py
```

### Step 3: Run Automated Tests
```powershell
python run_tests.py
```

### Step 4: Start Application
```powershell
# Terminal 1: Start backend
python backend/wsgi.py

# Terminal 2: Start frontend
cd frontend
python -m http.server 8000
```

### Step 5: Manual Testing
- Open http://localhost:8000/admin.html
- Login: `admin@resqtrack.com` / `admin123`
- Test all buttons and features

---

## 📊 What Gets Tested

### ✅ Automated Tests (100+ test cases)

#### Admin Dashboard Tests
- ✅ Admin login authentication
- ✅ View all cases, NGOs, volunteers, donations
- ✅ View hospitals, police stations, blood banks, fire stations
- ✅ View emergency contacts
- ✅ Add new hospitals
- ✅ Add new police stations
- ✅ Add new blood banks
- ✅ Add new fire stations
- ✅ Add new emergency contacts
- ✅ Approve NGO registrations
- ✅ Approve volunteer registrations
- ✅ Update case status
- ✅ CSV bulk upload for all services
- ✅ Authorization checks (JWT required)
- ✅ Error handling (invalid inputs)

#### Frontend Integration Tests
- ✅ Report case button functionality
- ✅ NGO registration form
- ✅ Volunteer registration form
- ✅ Donation submission
- ✅ Hospital listing
- ✅ Duplicate email prevention
- ✅ Required field validation

#### Core Functionality Tests
- ✅ Authentication & JWT tokens
- ✅ File upload with validation
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Error responses

---

## 🔧 Manual Testing Checklist

### Admin Dashboard (`/admin.html`)

#### Login
- [ ] Navigate to http://localhost:8000/admin.html
- [ ] Enter email: `admin@resqtrack.com`
- [ ] Enter password: `admin123`
- [ ] Click login (auto-login on page load)
- [ ] Verify statistics cards show numbers

#### View Data Tabs
- [ ] Click "Cases" tab - verify cases load
- [ ] Click "NGOs" tab - verify NGOs load
- [ ] Click "Volunteers" tab - verify volunteers load
- [ ] Click "Donations" tab - verify donations load
- [ ] Click "Hospitals" tab - verify hospitals load
- [ ] Click "Police Stations" tab - verify stations load
- [ ] Click "Blood Banks" tab - verify banks load
- [ ] Click "Fire Stations" tab - verify stations load
- [ ] Click "Emergency Contacts" tab - verify contacts load

#### Add New Records
- [ ] In Hospitals tab, click "➕ Add Hospital"
- [ ] Fill form and click map to select location
- [ ] Click "Save Location"
- [ ] Verify success toast appears
- [ ] Verify new hospital appears in table

- [ ] In Police tab, click "➕ Add Police Station"
- [ ] Fill form with station details
- [ ] Click "Save Location"
- [ ] Verify success toast

#### Map Views
- [ ] In Hospitals tab, click "🗺️ Map View"
- [ ] Verify map loads with markers
- [ ] Click marker to see popup
- [ ] Switch back to "📋 Table View"

- [ ] In Police tab, click "🗺️ Map View"
- [ ] Verify map loads
- [ ] Test marker interactions

#### CSV Import
- [ ] Click "🏥 Import Hospitals" button
- [ ] Select a CSV file (or download sample first)
- [ ] Click "Upload"
- [ ] Verify progress indicator
- [ ] Verify success message with import count
- [ ] Verify data appears in table

#### Approve Actions
- [ ] In NGOs tab, find pending NGO (badge: "Pending")
- [ ] Click approve button (if available)
- [ ] Verify status changes to "Approved"

- [ ] In Volunteers tab, find pending volunteer
- [ ] Click approve button
- [ ] Verify status changes

#### Refresh Data
- [ ] Click "🔄 Refresh" button (bottom right)
- [ ] Verify loading spinner appears
- [ ] Verify all data reloads
- [ ] Verify success toast

### Frontend Pages

#### Home Page (`/index.html`)
- [ ] Navigate to http://localhost:8000/index.html
- [ ] Verify hero section loads
- [ ] Verify statistics animate
- [ ] Click "🐾 Save a Life" button
- [ ] Verify redirects to report page

#### Report Page (`/report.html`)
- [ ] Fill reporter phone: `9999999999`
- [ ] Fill location: `Test City`
- [ ] Select animal type: `Dog`
- [ ] Select urgency: `High`
- [ ] Add notes: `Test case`
- [ ] Click "Submit Report"
- [ ] Verify success toast with case code
- [ ] Verify loading spinner during submission

#### Register Page (`/register.html`)
- [ ] Click "NGO" tab
- [ ] Fill NGO name, email, phone
- [ ] Click "Register NGO"
- [ ] Verify success toast

- [ ] Click "Volunteer" tab
- [ ] Fill volunteer details
- [ ] Click "Register Volunteer"
- [ ] Verify success toast

#### Donate Page (`/donate.html`)
- [ ] Fill donor name and email
- [ ] Enter amount: `1000`
- [ ] Select category: `Medical`
- [ ] Click "Donate Now"
- [ ] Verify success toast

#### Hospitals Page (`/hospitals.html`)
- [ ] Verify hospital list loads
- [ ] Verify map shows markers
- [ ] Click marker to see hospital details

---

## 🐛 Common Issues & Fixes

### Issue: Admin dashboard shows "Loading..." forever
**Cause**: Backend not running or CORS error
**Fix**:
1. Check backend is running: `python backend/wsgi.py`
2. Check browser console for errors
3. Verify `ALLOWED_ORIGINS` in `.env` includes `http://localhost:8000`

### Issue: "401 Unauthorized" errors
**Cause**: Admin user not seeded or JWT expired
**Fix**:
1. Run `python seed_admin.py`
2. Refresh page to re-login
3. Check browser console for token

### Issue: "Network error" on all requests
**Cause**: Backend not running or wrong port
**Fix**:
1. Verify backend at http://localhost:5000/health
2. Check `API_BASE` in `frontend/assets/js/api.js`

### Issue: Add buttons don't work
**Cause**: Modal JavaScript not loaded
**Fix**:
1. Check browser console for errors
2. Verify Bootstrap JS is loaded
3. Clear browser cache

### Issue: CSV upload fails
**Cause**: Wrong CSV format or missing columns
**Fix**:
1. Download sample CSV first
2. Match column names exactly
3. Check for required fields

### Issue: Map doesn't load
**Cause**: Leaflet not loaded or geocoding failed
**Fix**:
1. Check browser console
2. Verify internet connection (for map tiles)
3. Check location field has valid city name

### Issue: Tests fail with import errors
**Cause**: Virtual environment not activated
**Fix**:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📈 Test Results Interpretation

### All Tests Pass ✅
```
✅ PASSED - Authentication Tests
✅ PASSED - Case Management Tests
✅ PASSED - Upload Tests
✅ PASSED - Admin Dashboard Tests
✅ PASSED - Frontend Integration Tests

🎉 All tests passed!
```
**Action**: Proceed to manual testing

### Some Tests Fail ❌
```
❌ FAILED - Admin Dashboard Tests
```
**Action**:
1. Read error messages carefully
2. Check if database is initialized
3. Verify admin user exists
4. Run failing test individually: `pytest tests/test_e2e_admin.py::test_name -v`

---

## 🔍 Debugging Tips

### Backend Debugging
```powershell
# Check if backend is running
curl http://localhost:5000/health

# View backend logs
python backend/wsgi.py
# Watch for errors in console
```

### Frontend Debugging
```
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for red errors
4. Check Network tab for failed requests
5. Verify API_BASE is correct
```

### Database Debugging
```powershell
# Check if admin exists
python
>>> from backend.app import create_app
>>> from backend.app.models import Admin
>>> app = create_app()
>>> with app.app_context():
...     admin = Admin.query.filter_by(email='admin@resqtrack.com').first()
...     print(admin)
```

---

## 🎯 Success Criteria

### Backend Tests
- ✅ All pytest tests pass
- ✅ No import errors
- ✅ No database errors
- ✅ JWT authentication works

### Frontend Tests
- ✅ All pages load without errors
- ✅ All buttons respond
- ✅ Forms submit successfully
- ✅ Toast notifications appear
- ✅ Loading spinners show

### Admin Dashboard
- ✅ Login works
- ✅ All 9 tabs load data
- ✅ Statistics show correct counts
- ✅ Add buttons open modals
- ✅ Save buttons create records
- ✅ CSV upload works
- ✅ Map views load
- ✅ Refresh button works

---

## 📞 Need Help?

### Check Logs
1. Backend terminal for API errors
2. Browser console for frontend errors
3. Network tab for failed requests

### Verify Setup
```powershell
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | findstr Flask

# Check database
flask db current  # Should show migration version
```

### Reset Everything
```powershell
# Delete database
rm resqtrack.db

# Re-initialize
flask db upgrade
python seed_admin.py

# Restart servers
python backend/wsgi.py
cd frontend && python -m http.server 8000
```

---

## ✨ Next Steps After Testing

1. ✅ All tests pass → Deploy to production
2. ❌ Tests fail → Fix issues and re-test
3. 🐛 Bugs found → Create GitHub issues
4. 💡 New features → Add tests first

---

## 📚 Additional Resources

- **API Documentation**: See `README.md`
- **Test Guide**: See `TEST_GUIDE.md`
- **Architecture**: See `docs/architecture/`
- **Sample Data**: See `sample_data/` folder

---

**Happy Testing! 🎉**
