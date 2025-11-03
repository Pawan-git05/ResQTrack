  # ResQTrack

ResQTrack is a lightweight, full‑stack web app that coordinates animal rescue across citizens, NGOs, volunteers, animal hospitals and donors. Citizens can quickly report an injured animal, NGOs and volunteers can act, hospitals can be listed, and donors can contribute — all tracked end‑to‑end.

The project is intentionally simple to run locally (no heavy frontend tooling) but still production‑minded on the backend (JWT auth, migrations, mail, uploads, CORS).

## What this project does
- Citizens submit rescue reports (with optional photo/video) to create an incident.
- NGOs/volunteers coordinate response and status updates.
- Hospital directory helps route animals to the right care.
- Donors can record donations with automatic email receipts (if SMTP configured).
- Admin/NGO actions use JWT for protected routes.
- **NEW**: Comprehensive data integration system for emergency services (police, fire, blood banks, etc.)
- **NEW**: Interactive data dashboard for importing, visualizing, and managing multiple datasets.

## Tech Stack
- **Backend**: Flask, SQLAlchemy, Alembic (Flask‑Migrate), JWT, Flask‑Mail, Flask‑CORS, SQLite (default) or any SQL via `DATABASE_URL`.
- **Frontend**: HTML + Bootstrap + vanilla JS. No build step. Served as static files.

## Quick Start (Windows‑friendly)

### 1) Prerequisites
- Python 3.11+
- Optional: MySQL 8+ if you plan to use MySQL instead of SQLite

### 2) Setup Python environment
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Environment file (optional): copy and adjust if you maintain one.
```bash
# If you have an example env
# copy .env.example .env   (PowerShell: cp .env.example .env)
```

Key environment variables (see `backend/config.py` for defaults):
- `SECRET_KEY`, `JWT_SECRET_KEY`
- `DATABASE_URL` (omit to use local SQLite `resqtrack.db`)
- `MAIL_*` (SMTP settings for email receipts)
- `CORS_ORIGINS` (defaults to `*` for local/dev)

### 3) Initialize the database
SQLite is default; no server needed.
```bash
set FLASK_APP=backend/wsgi.py
python -m flask db upgrade
```

Optional: load sample data (inspect `docs/sql/sample_data.sql`).

**NEW**: Import comprehensive emergency services data:
```bash
python import_sample_data.py
```

### 4) Run the backend (API)
```bash
python backend/wsgi.py
```
The API will be available at `http://localhost:5000` (health check at `/health`).

### 5) Run the frontend (static)
From the `frontend/` directory, serve files with a simple HTTP server:
```bash
cd frontend
python -m http.server 8000
```
Visit `http://localhost:8000/index.html`.

**NEW**: Access the Data Dashboard at `http://localhost:8000/data-dashboard.html` for:
- Import/export CSV datasets
- Visualize emergency services distribution
- Manage NGOs, volunteers, hospitals, police stations, blood banks, fire stations
- View real-time statistics and analytics

Front‑to‑back integration is configured via `frontend/assets/js/api.js`:
```js
const API_BASE = 'http://localhost:5000';
```

### Frontend UX notes
- Images are responsive (`img { max-width: 100%; height: auto; }`) and hero/card media use object‑fit to avoid distortion.
- The story popup on CTA buttons is disabled; buttons now navigate directly to their target pages.

## End‑user flows
- **Report**: `Report` page posts a case with optional file; returns a `case_code` for reference.
- **Donate**: `Donate` page records a donation and sends a receipt email when SMTP is configured.
- **Register**: `Register` page has tabs for NGO and Volunteer applications.
- **Hospitals**: `Hospitals` page lists directory entries; admins/NGOs can add via API.

## API Reference

Base URL: `http://localhost:5000`

### Health
- `GET /health` → `{ status: "ok" }`

### Auth
- `POST /auth/login` body `{ email, password, role }` → `{ access_token }`
  - roles: `ADMIN`, `NGO`, `VOLUNTEER`

### Cases
- `POST /cases` (public)
  - Accepts JSON or multipart form data. Fields: `reporter_name?`, `reporter_phone`, `reporter_email?`, `location`, `latitude?`, `longitude?`, `animal_type?`, `urgency?`, `notes?`, and optional `file`.
  - Response `201`: `{ message, case_id, case_code, media_url? }`
- `PATCH /cases/<case_id>/status` (JWT required)
  - Body `{ status }` where status is one of backend `CaseStatus` enums.

### Registrations
- `POST /register/ngo` → `201 { message, ngo_id }`
- `POST /register/volunteer` → `201 { message, volunteer_id }`
  - `409` on duplicate `email`.

### Hospitals
- `GET /hospitals` → `{ items: [...] }`
- `POST /hospitals` (JWT required) → `201 { message, id }`

### Donations
- `POST /donations` → `201 { message, id }`
  - If `donor_email` is provided and SMTP is configured, a receipt email is sent.

### Uploads
- `POST /uploads` (multipart, field `file`) → `201 { filename, url }`
- `GET /uploads/<filename>` → serves the uploaded file

### Data Integration (NEW)
- `POST /data/import/<type>` (JWT required) → `201 { message, stats }`
  - types: `ngos`, `volunteers`, `hospitals`, `police-stations`, `blood-banks`, `fire-stations`
- `GET /data/export/<type>` (JWT required) → `200 { message, download_url }`
- `GET /data/statistics` (JWT required) → `200 { statistics, location_distribution }`
- `GET /data/emergency-contacts` → `200 { contacts: [...] }`
- `GET /data/nearby-services?location=<city>&service_type=<type>` → `200 { services: [...] }`

### Common Errors
- `400` Missing/invalid fields
- `401` Invalid credentials or missing token
- `409` Duplicate resource (e.g., `email` already registered)

## Data model (high‑level)
- `AnimalCase` with `case_code`, contact/location, type, urgency, notes, optional `media_url`, and `status`.
- `NGO`, `Volunteer`, `Hospital`, `Donation` entities with essential fields.
- **NEW**: `PoliceStation`, `BloodBank`, `FireStation`, `EmergencyContact` for comprehensive emergency services.
- See `docs/architecture/ERD.md` and `backend/app/models.py` for complete definitions.

## Configuration & Operations
- CORS is enabled (credentials supported). Tune origins via `CORS_ORIGINS`.
- File uploads stored in `uploads/` by default; override `UPLOAD_FOLDER`. You can front this with a CDN or adapt to S3.
- Mail uses standard SMTP. For Gmail, use App Passwords and set `MAIL_USERNAME`/`MAIL_PASSWORD`.
- Migrations are managed via Alembic (Flask‑Migrate). Commit migration scripts in `migrations/` for schema changes.

## Project Structure
```
backend/
  app/
    routes/
    models.py
    extensions.py
    utils.py
    mailer.py
    data_integration.py  # NEW: Data import/export system
  config.py
  wsgi.py
frontend/
  index.html report.html register.html donate.html hospitals.html data-dashboard.html  # NEW
  assets/css/styles.css
  assets/js/api.js app.js data-dashboard.js  # NEW
docs/
  PRD.md
  architecture/ERD.md, DFD.md
  sql/schema.sql, sample_data.sql
  DATA_INTEGRATION.md  # NEW: Comprehensive data integration guide
  DATA_INTEGRATION_QUICK_REFERENCE.md  # NEW: Quick reference
sample_data/  # NEW: Sample CSV files
  ngos.csv volunteers.csv hospitals.csv police_stations.csv blood_banks.csv fire_stations.csv
import_sample_data.py  # NEW: Data import script
```

## Contributing
1. Fork + branch from `main`.
2. Make changes with clear commits.
3. If you change the database, add a migration: `flask db migrate -m "..."` then `flask db upgrade` locally and include the generated script.
4. Open a PR describing the change, rationale, and testing steps.

## License
MIT
