  # ResQTrack
ResQTrack is a small, friendly tool to help people, NGOs, volunteers, and hospitals coordinate animal rescues. A citizen can report an injured animal (with an optional photo/video), responders can pick it up from there, and you can track things end‑to‑end. Donors can chip in too.

Under the hood it’s a Flask API with a simple static frontend (HTML/JS/CSS). It’s easy to run locally, and it comes with production basics like JWT auth, database migrations, CORS, upload validation, logging, and optional Docker.

## Features
- Report animal cases (optionally attach media)
- Sign in with roles: ADMIN / NGO / VOLUNTEER (JWT)
- Register NGOs and Volunteers
- Hospitals directory and donation records
- Centralized JSON error responses (no HTML error pages)
- Sensible rate limiting (login/registration)
- CORS that you can control via environment variables
- Logging to console (and file if you want)
- Tests via pytest and CI via GitHub Actions

## Quick Start (local)

1) Install dependencies
```
python -m venv .venv
".venv\\Scripts\\Activate.ps1"  # Windows
# source .venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

2) Configure environment
```
cp .env.example .env  # or copy manually on Windows
```
Keep defaults for SQLite, and set `ALLOWED_ORIGINS=http://localhost:8000`.

3) Initialize the database
```
set FLASK_APP=backend/wsgi.py   # Windows
flask db upgrade
# macOS/Linux: export FLASK_APP=backend/wsgi.py && flask db upgrade
```

4) Run the app
```
python backend/wsgi.py   # API at http://localhost:5000
cd frontend && python -m http.server 8000   # Frontend at http://localhost:8000
```

That’s it. If you want containers, use `docker-compose up --build` instead.

## Folder Structure
```
ResQTrack/
  backend/
    app/
      routes/            # API blueprints (auth, cases, uploads, etc.)
      models.py          # SQLAlchemy models
      extensions.py      # Flask extensions (db, jwt, cors, limiter, mail)
      utils.py           # Helpers
      mailer.py          # Email utilities
      data_integration.py# Bulk data import/export utilities
    config.py            # App configuration
    logging_config.py    # Logging setup (RotatingFileHandler + console)
    wsgi.py              # App entrypoint for Gunicorn/Flask
  frontend/
    assets/css/          # Styles (includes toasts, spinners, theme)
    assets/js/           # API client + UI helpers (toasts, loading overlay)
    *.html               # Static pages (index, report, register, donate, admin, data-dashboard)
  docs/                  # Docs, SQL schema, ERD/DFD
  migrations/            # Alembic migration scripts
  tests/                 # Pytest suite
  .github/workflows/ci.yml
  .env.example           # Example environment file
  Dockerfile
  docker-compose.yml
  requirements.txt
  README.md
```

## Setup

### Prerequisites
- Python 3.11+
- Optional: MySQL 8+ (if not using SQLite)
- Optional: Docker and Docker Compose

### 1) Clone and create a virtual environment
Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
macOS/Linux (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment
Copy the example env and adjust:
```bash
cp .env.example .env    # Windows PowerShell: cp .env.example .env
```
Important variables:
- `SECRET_KEY`, `JWT_SECRET_KEY`
- `DATABASE_URL` (defaults to SQLite if omitted)
- `MAIL_*` for SMTP
- `ALLOWED_ORIGINS` for CORS in production (comma‑separated list)
- `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH` (bytes)
- Optional S3: `AWS_S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- Optional rate limit storage: `RATELIMIT_STORAGE_URI` (e.g., `redis://redis:6379`)

### 3) Initialize the database
SQLite (default):
```bash
set FLASK_APP=backend/wsgi.py       # Windows
flask db upgrade
```
```bash
export FLASK_APP=backend/wsgi.py    # macOS/Linux
flask db upgrade
```
For MySQL, set `DATABASE_URL` to e.g. `mysql://user:password@localhost:3306/resqtrack` and run `flask db upgrade`.

### 4) Run the app locally
```bash
python backend/wsgi.py
```
Backend: http://localhost:5000

Frontend (static):
```bash
cd frontend
python -m http.server 8000
```
Visit http://localhost:8000/index.html

## Run with Docker
Build and start the full stack (Flask + MySQL + Redis):
```bash
docker-compose up --build
```
- API: http://localhost:5000
- MySQL: localhost:3306
- Redis: localhost:6379

Notes:
- By default, the app uses `DATABASE_URL` from your `.env`. If not set, it falls back to SQLite.
- Volumes persist uploads and logs.
- CORS can be controlled via `ALLOWED_ORIGINS` env (comma‑separated).

## Example API Usage
Login:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@resqtrack.com", "password": "admin123", "role": "ADMIN"}'
```
Report a case (JSON):
```bash
curl -X POST http://localhost:5000/cases \
  -H "Content-Type: application/json" \
  -d '{"reporter_phone":"9999999999","location":"MG Road","animal_type":"Dog","urgency":"Low"}'
```
Report a case with media (multipart):
```bash
curl -X POST http://localhost:5000/cases \
  -F file=@/path/to/photo.jpg \
  -F reporter_phone=9999999999 -F location="MG Road"
```
Upload file directly:
```bash
curl -X POST http://localhost:5000/uploads -F file=@/path/to/photo.jpg
```

## Auth Roles
| Role       | Who | Notes |
|------------|-----|-------|
| ADMIN      | Platform admin | Can access admin endpoints, manage resources |
| NGO        | NGO member     | Can access NGO workflows |
| VOLUNTEER  | Volunteer      | Can access volunteer workflows |

JWT identity payload includes `id`, `email`, and `role`.

## Security Hardening
- CORS restricted via `ALLOWED_ORIGINS` (production)
- Upload validation: extension whitelist, MIME type check, file size limit, sanitized filename
- Global JSON error handlers for all exceptions (no HTML error pages)
- Rate limiting: `5/min` for `/auth/login`, `10/hour` for registrations

## Testing & Linting
- Run tests:
```bash
pytest -q
```
- Lint:
```bash
flake8 backend
```
CI (GitHub Actions) runs on push/PR: Python 3.11, installs deps, runs `flake8` and `pytest`.

## Troubleshooting
- 401 Unauthorized: Ensure `Authorization: Bearer <token>` header is set for protected endpoints.
- CORS errors in browser: set `ALLOWED_ORIGINS` to include your frontend origin (e.g., `http://localhost:8000`).
- File upload fails: verify extension/MIME type and that `MAX_CONTENT_LENGTH` isn’t exceeded.
- MySQL connection errors in Docker: wait for db to be healthy, or check `DATABASE_URL` and credentials.
- Emails not sent: verify SMTP credentials and allow provider‑specific requirements (e.g., Gmail App Passwords).
- Rate limit exceeded: API returns 429; reduce frequency or configure `RATELIMIT_STORAGE_URI`.
