# ResQTrack Data Integration - Quick Reference

## 🚀 Quick Start Commands

```bash
# 1. Apply database migrations
python -m flask --app backend/wsgi.py db upgrade

# 2. Import sample data
python import_sample_data.py

# 3. Start backend server
python backend/wsgi.py

# 4. Start frontend (new terminal)
cd frontend && python -m http.server 8000
```

## 📊 Available Datasets

| Dataset | File | Records | Description |
|---------|------|---------|-------------|
| NGOs | `sample_data/ngos.csv` | 5 | Animal rescue organizations |
| Volunteers | `sample_data/volunteers.csv` | 5 | Individual volunteers |
| Hospitals | `sample_data/hospitals.csv` | 5 | Animal hospitals |
| Police Stations | `sample_data/police_stations.csv` | 5 | Emergency police services |
| Blood Banks | `sample_data/blood_banks.csv` | 5 | Blood donation centers |
| Fire Stations | `sample_data/fire_stations.csv` | 5 | Fire and rescue services |

## 🔗 API Endpoints

### Public Endpoints (No Auth Required)
- `GET /data/emergency-contacts` - Emergency contact directory
- `GET /data/nearby-services?location=<city>&service_type=<type>` - Find nearby services

### Protected Endpoints (JWT Required)
- `POST /data/import/<type>` - Import CSV data
- `GET /data/export/<type>` - Export CSV data
- `GET /data/statistics` - Get analytics

## 📈 Dashboard Features

### Data Dashboard (`/data-dashboard.html`)
- **Statistics Cards**: Real-time entity counts
- **Import Interface**: CSV file upload
- **Charts**: Service distribution visualization
- **Emergency Directory**: Searchable contacts
- **Export Tools**: Download data

### Navigation
- Main menu: "📈 Data Dashboard"
- Admin page: "Data Dashboard" link
- Direct URL: `http://localhost:8000/data-dashboard.html`

## 🗂️ CSV Format Requirements

### Required Headers
- **NGOs**: `name,email,phone,location,operating_zones,approved`
- **Volunteers**: `name,email,phone,location,expertise,availability,approved`
- **Hospitals**: `name,address,phone,location,is_24x7,treatment_types`
- **Police**: `name,address,phone,location,station_code,is_24x7,jurisdiction,officer_in_charge`
- **Blood Banks**: `name,address,phone,location,is_24x7,blood_types_available,contact_person,license_number`
- **Fire Stations**: `name,address,phone,location,station_code,is_24x7,equipment_available,chief_officer`

### Data Types
- **Boolean**: `true`/`false` for `is_24x7`, `approved`
- **Lists**: Comma-separated values in quotes: `"item1,item2,item3"`
- **Phone**: Include country code: `+91-9876543210`
- **Email**: Valid email format required

## 🔧 Troubleshooting

### Import Issues
```bash
# Check file format
head -1 sample_data/ngos.csv

# Validate CSV
python -c "import csv; csv.DictReader(open('sample_data/ngos.csv'))"

# Check database
python -c "from backend.app import create_app; from backend.app.extensions import db; app = create_app(); app.app_context().push(); print(db.engine.execute('SELECT COUNT(*) FROM ngos').scalar())"
```

### API Issues
```bash
# Test public endpoint
curl http://localhost:5000/data/emergency-contacts

# Test with auth (replace <token>)
curl -H "Authorization: Bearer <token>" http://localhost:5000/data/statistics
```

### Frontend Issues
- Check browser console for JavaScript errors
- Verify API base URL in `frontend/assets/js/api.js`
- Clear browser cache
- Check CORS settings

## 📋 Sample Data Structure

### Emergency Contacts (Auto-added)
- National Emergency Number: `100` (Police)
- Fire Emergency Number: `101` (Fire)
- Medical Emergency Number: `108` (Medical)
- Disaster Management Helpline: `108` (Disaster)

### Location Coverage
- **Mumbai**: NGOs, Volunteers, Hospitals, Police, Blood Banks, Fire Stations
- **Delhi**: NGOs, Volunteers, Hospitals, Police, Blood Banks, Fire Stations
- **Bangalore**: NGOs, Volunteers, Hospitals, Police, Blood Banks, Fire Stations
- **Chennai**: NGOs, Volunteers, Hospitals, Police, Blood Banks, Fire Stations
- **Pune**: NGOs, Volunteers, Hospitals, Police, Blood Banks, Fire Stations

## 🎯 Use Cases

### For Administrators
- Import real-world emergency service data
- Monitor service coverage and distribution
- Export data for analysis and reporting
- Manage emergency contact directory

### For Citizens
- Find nearby emergency services
- Access emergency contact information
- Report animal rescue cases
- Coordinate with local NGOs and volunteers

### For NGOs/Volunteers
- Register and manage volunteer networks
- Coordinate rescue operations
- Access hospital and service directories
- Track case assignments

## 🔄 Data Flow

1. **CSV Upload** → Data Dashboard
2. **Validation** → Backend API
3. **Import** → Database
4. **Statistics** → Dashboard Charts
5. **Export** → CSV Download

## 📱 Mobile Support

The data dashboard is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones
- Progressive Web App (PWA) ready

## 🔐 Security Notes

- JWT tokens required for data modification
- Public endpoints for emergency services
- Input validation and sanitization
- CORS configured for local development
- File upload security implemented
