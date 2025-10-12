# ResQTrack

ResQTrack is a web-based coordination platform for animal rescue operations connecting citizens, NGOs, volunteers, hospitals, and donors.

## Tech Stack
- Backend: Python Flask, SQLAlchemy, SQLite by default (override to MySQL with `DATABASE_URL`), JWT, Mail
- Frontend: HTML/CSS/JS (Bootstrap)

## Getting Started

### 1) Prerequisites
- Python 3.11+
- Optional: MySQL 8+ (only if you set `DATABASE_URL` to a MySQL URI)

### 2) Clone and Install
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```

SQLite is used by default. To use MySQL, set `DATABASE_URL` like `mysql://user:pass@host:3306/resqtrack` and install `mysqlclient` (requires MSVC build tools on Windows).

### 3) Database Migrations
```bash
set FLASK_APP=backend/wsgi.py
python -m flask db init
python -m flask db migrate -m "init"
python -m flask db upgrade
```

(Optional) Load sample data:
```bash
# With SQLite, use app endpoints or insert manually via scripts
# With MySQL:
# mysql -u <user> -p resqtrack < docs/sql/sample_data.sql
```

### 4) Run Server
```bash
python backend/wsgi.py
```
Visit `http://localhost:5000/health`.

### 5) Frontend
Open `frontend/index.html` in your browser. Forms call the backend APIs.

## API Overview
- GET `/health`
- POST `/auth/login`
- POST `/cases`, PATCH `/cases/<id>/status`
- POST `/register/ngo`, POST `/register/volunteer`
- GET/POST `/hospitals`
- POST `/donations`
- POST `/uploads`, GET `/uploads/<filename>`

## Project Structure
```
backend/
  app/
    routes/
    models.py
    extensions.py
    utils.py
    mailer.py
  config.py
  wsgi.py
frontend/
  index.html report.html register.html donate.html hospitals.html
  assets/css styles.css
  assets/js api.js
docs/
  PRD.md
  architecture/ERD.md, DFD.md
  sql/schema.sql, sample_data.sql
```

## Notes
- Emails use SMTP; for Gmail, enable App Passwords and set `MAIL_USERNAME`/`MAIL_PASSWORD`.
- File uploads are stored under `uploads/`. For S3, configure AWS env vars and extend storage logic.

## License
MIT
