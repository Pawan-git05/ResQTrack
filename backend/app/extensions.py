from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail


db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
jwt: JWTManager = JWTManager()
cors: CORS = CORS()
mail: Mail = Mail()


@jwt.user_identity_loader
def user_identity_lookup(user):
    """Convert user identity to string for JWT"""
    if isinstance(user, dict):
        return str(user.get('id', ''))
    return str(user)