# syntax=docker/dockerfile:1.6
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

# Install system deps for mysqlclient and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	default-libmysqlclient-dev \
	pkg-config \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY backend ./backend
COPY frontend ./frontend
COPY migrations ./migrations
COPY backend/wsgi.py ./backend/wsgi.py

# Create runtime dirs
RUN mkdir -p /app/uploads /app/logs

ENV PORT=5000
EXPOSE 5000

# Default to production
ENV FLASK_ENV=production

# Gunicorn config: 2-4 workers based on CPUs
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "60", "backend.wsgi:application"]
