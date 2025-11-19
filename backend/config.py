import os
from datetime import timedelta
from dotenv import load_dotenv


# Load environment from project .env (if present)
load_dotenv()


class Config:
	SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
	JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

	# Read database URL from environment (.env or system env). No SQLite fallback.
	SQLALCHEMY_DATABASE_URI: str | None = os.getenv("DATABASE_URL")
	SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

	# JWT
	JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=8)

	# CORS
	CORS_SUPPORTS_CREDENTIALS: bool = True
	# Prefer ALLOWED_ORIGINS for production; fallback to CORS_ORIGINS or '*'
	_cors_origins_env = os.getenv(
		"ALLOWED_ORIGINS",
		os.getenv("CORS_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500"),
	)
	CORS_ORIGINS: str | list[str] = (
		_cors_origins_env.split(",") if "," in _cors_origins_env else _cors_origins_env
	)

	# Mail
	MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
	MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
	MAIL_USE_TLS: bool = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
	MAIL_USE_SSL: bool = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
	MAIL_USERNAME: str | None = os.getenv("MAIL_USERNAME")
	MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
	MAIL_DEFAULT_SENDER: tuple[str, str] | str | None = os.getenv("MAIL_DEFAULT_SENDER")

	# Uploads
	UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", os.path.abspath("uploads"))
	MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16MB

	# Storage (optional S3)
	AWS_S3_BUCKET: str | None = os.getenv("AWS_S3_BUCKET")
	AWS_ACCESS_KEY_ID: str | None = os.getenv("AWS_ACCESS_KEY_ID")
	AWS_SECRET_ACCESS_KEY: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")
	AWS_REGION: str | None = os.getenv("AWS_REGION")

	# Rate limiting storage (optional Redis URL). Flask-Limiter will use in-memory if not provided.
	RATELIMIT_STORAGE_URI: str | None = os.getenv("RATELIMIT_STORAGE_URI")
