from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
mail = Mail()

# We will initialize limiter safely later
limiter = Limiter(key_func=get_remote_address, enabled=True)


def init_limiter(app):
    """
    Safe Rate Limiter initialization:
    - Disables limiter if RATELIMIT_ENABLED=false
    - Falls back to memory:// if Redis URI fails
    - Prevents crashes
    """
    enabled = app.config.get("RATELIMIT_ENABLED", "true").lower() == "true"
    if not enabled:
        print("⚠ Rate Limiter DISABLED (RATELIMIT_ENABLED=false)")
        return

    storage_uri = app.config.get("RATELIMIT_STORAGE_URI", "memory://")

    # If Redis is set but not installed, switch to memory backend
    if storage_uri.startswith("redis://"):
        try:
            import redis  # noqa
        except Exception:
            print("⚠ Redis not installed. Switching RateLimiter to memory:// backend.")
            storage_uri = "memory://"

    limiter._storage_uri = storage_uri

    try:
        limiter.init_app(app)
        print(f"✓ Rate Limiter initialized using: {storage_uri}")
    except Exception as e:
        print(f"⚠ Rate Limiter failed: {e}. Falling back to memory://")
        limiter._storage_uri = "memory://"
        limiter.init_app(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    """Convert user identity to a string for JWT"""
    if isinstance(user, dict):
        return str(user.get("id", ""))
    return str(user)
