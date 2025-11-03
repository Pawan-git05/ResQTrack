# 🚀 ResQTrack - Quick Start Guide

## ⚡ 3-Minute Setup

### 1. Install Dependencies (1 min)
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Setup Database (30 sec)
```powershell
set FLASK_APP=backend/wsgi.py
flask db upgrade
python seed_admin.py
```

### 3. Run Tests (1 min)
```powershell
python run_tests.py
```

### 4. Start Application (30 sec)
```powershell
# Terminal 1: Backend
python backend/wsgi.py

# Terminal 2: Frontend (new terminal)
cd frontend
python -m http.server 8000
```

### 5. Access & Test
- **Admin Dashboard**: http://localhost:8000/admin.html
- **Login**: `admin@resqtrack.com` / `admin123`
- **Frontend**: http://localhost:8000/index.html

---

## 📋 What You Get

### ✅ Fully Functional Admin Dashboard
- View all cases, NGOs, volunteers, donations
- View hospitals, police stations, blood banks, fire stations
- Add new records with map picker
- Approve NGO/Volunteer registrations
- Update case status
- CSV bulk import
- Map visualization
- Real-time statistics

### ✅ Public Frontend
- Report animal cases
- Register as NGO or Volunteer
- Make donations
- View hospital directory
- Beautiful UI with toasts & loading states

### ✅ Production-Ready Backend
- JWT authentication
- Rate limiting (5/min login, 10/hr registration)
- CORS configured
- File upload validation
- Global error handling
- Logging (console + file)
- 100+ automated tests

---

## 🎯 Test All Features

### Admin Dashboard Tests
```
✅ Login with admin credentials
✅ View 9 different data tabs
✅ Add hospitals with map picker
✅ Add police stations
✅ CSV import for bulk data
✅ Approve pending NGOs/Volunteers
✅ Update case status
✅ Switch between table/map views
✅ Refresh data
```

### Frontend Tests
```
✅ Report case from homepage
✅ Register as NGO
✅ Register as Volunteer
✅ Submit donation
✅ View hospitals on map
✅ Form validation
✅ Toast notifications
✅ Loading spinners
```

---

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check if port 5000 is free
netstat -ano | findstr :5000

# Kill process if needed
taskkill /PID <PID> /F

# Restart
python backend/wsgi.py
```

### Frontend shows "Loading..."
```
1. Check backend is running: http://localhost:5000/health
2. Check browser console for errors (F12)
3. Verify CORS: Add http://localhost:8000 to ALLOWED_ORIGINS in .env
```

### Tests fail
```powershell
# Ensure venv is activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# Run specific test
pytest tests/test_e2e_admin.py -v
```

### Database errors
```powershell
# Reset database
rm resqtrack.db
flask db upgrade
python seed_admin.py
```

---

## 📁 Project Structure

```
ResQTrack/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── models.py        # Database models
│   │   ├── extensions.py    # Flask extensions
│   │   └── __init__.py      # App factory
│   ├── config.py            # Configuration
│   ├── logging_config.py    # Logging setup
│   └── wsgi.py              # Entry point
├── frontend/
│   ├── assets/
│   │   ├── css/styles.css   # Styles + toasts + spinners
│   │   └── js/
│   │       ├── api.js       # API client
│   │       └── app.js       # UI utilities
│   ├── admin.html           # Admin dashboard
│   ├── index.html           # Homepage
│   ├── report.html          # Report case
│   ├── register.html        # NGO/Volunteer registration
│   ├── donate.html          # Donations
│   └── hospitals.html       # Hospital directory
├── tests/                   # 100+ automated tests
├── .env.example             # Environment template
├── Dockerfile               # Production container
├── docker-compose.yml       # Full stack (Flask + MySQL + Redis)
├── requirements.txt         # Python dependencies
├── seed_admin.py            # Database seeder
├── run_tests.py             # Test runner
└── README.md                # Full documentation
```

---

## 🔑 Default Credentials

### Admin User
- **Email**: `admin@resqtrack.com`
- **Password**: `admin123`
- **Access**: Full admin dashboard

### Sample Data
- 3 animal cases
- 2 NGOs (1 approved, 1 pending)
- 2 volunteers (1 approved, 1 pending)
- 2 donations
- 2 hospitals

---

## 🚢 Deploy to Production

### Option 1: Docker
```bash
docker-compose up --build
```

### Option 2: Manual
```bash
# Set production env
export FLASK_ENV=production
export SECRET_KEY=<strong-secret>
export JWT_SECRET_KEY=<strong-jwt-secret>
export DATABASE_URL=mysql://user:pass@host:3306/resqtrack
export ALLOWED_ORIGINS=https://yourdomain.com

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 3 backend.wsgi:application
```

---

## 📚 Documentation

- **Full README**: `README.md`
- **Testing Guide**: `TESTING_README.md`
- **Test Details**: `TEST_GUIDE.md`
- **API Docs**: See README.md "API Reference" section

---

## ✨ Features Checklist

### Security ✅
- [x] JWT authentication
- [x] Rate limiting
- [x] CORS restriction
- [x] File upload validation
- [x] Password hashing
- [x] Global error handling

### Developer Experience ✅
- [x] `.env.example` template
- [x] Comprehensive README
- [x] 100+ automated tests
- [x] GitHub Actions CI
- [x] Docker support
- [x] Logging configured

### Frontend UX ✅
- [x] Toast notifications
- [x] Loading spinners
- [x] Form validation
- [x] Responsive design
- [x] Map integration
- [x] Modern UI

### Admin Dashboard ✅
- [x] Multi-tab interface
- [x] CRUD operations
- [x] CSV bulk import
- [x] Map visualization
- [x] Real-time stats
- [x] Approval workflows

---

## 🎉 You're All Set!

Your ResQTrack instance is now:
- ✅ Secure
- ✅ Tested
- ✅ Dockerized
- ✅ Production-ready
- ✅ Developer-friendly

**Next Steps**:
1. Customize branding in frontend
2. Configure SMTP for email receipts
3. Set up production database
4. Deploy to cloud (AWS, Azure, etc.)
5. Add custom features

---

**Need Help?** Check `TESTING_README.md` for detailed troubleshooting.
