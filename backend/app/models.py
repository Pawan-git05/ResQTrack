from datetime import datetime
from enum import Enum
from .extensions import db


class UserRole(str, Enum):
	ADMIN = "ADMIN"
	NGO = "NGO"
	VOLUNTEER = "VOLUNTEER"
	HOSPITAL = "HOSPITAL"
	CITIZEN = "CITIZEN"


class TimestampMixin:
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	updated_at = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
	)


class Admin(db.Model, TimestampMixin):
	__tablename__ = "admins"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	name = db.Column(db.String(255), nullable=False)
	is_superadmin = db.Column(db.Boolean, default=False, nullable=False)


class NGO(db.Model, TimestampMixin):
	__tablename__ = "ngos"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	phone = db.Column(db.String(30), nullable=False)
	location = db.Column(db.String(255), nullable=True)
	operating_zones = db.Column(db.Text, nullable=True)
	approved = db.Column(db.Boolean, default=False, nullable=False)

	volunteers = db.relationship("Volunteer", back_populates="ngo", lazy=True)
	cases = db.relationship("AnimalCase", back_populates="ngo", lazy=True)


class Volunteer(db.Model, TimestampMixin):
	__tablename__ = "volunteers"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	phone = db.Column(db.String(30), nullable=False)
	location = db.Column(db.String(255), nullable=True)
	expertise = db.Column(db.String(255), nullable=True)  # pickup, first aid, foster
	availability = db.Column(db.String(255), nullable=True)
	approved = db.Column(db.Boolean, default=False, nullable=False)
	ngo_id = db.Column(db.Integer, db.ForeignKey("ngos.id"), nullable=True)

	ngo = db.relationship("NGO", back_populates="volunteers")
	assigned_cases = db.relationship(
		"AnimalCase", back_populates="assigned_volunteer", foreign_keys="AnimalCase.assigned_volunteer_id", lazy=True
	)


class Hospital(db.Model, TimestampMixin):
	__tablename__ = "hospitals"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	address = db.Column(db.String(255), nullable=True)
	phone = db.Column(db.String(30), nullable=True)
	location = db.Column(db.String(255), nullable=True)
	is_24x7 = db.Column(db.Boolean, default=False, nullable=False)
	treatment_types = db.Column(db.String(255), nullable=True)  # surgery, first aid, etc

	cases = db.relationship("AnimalCase", back_populates="hospital", lazy=True)


class CaseStatus(str, Enum):
	PENDING = "PENDING"
	IN_PROGRESS = "IN_PROGRESS"
	RESCUED = "RESCUED"
	CLOSED = "CLOSED"


class AnimalType(str, Enum):
	DOG = "Dog"
	CAT = "Cat"
	BIRD = "Bird"
	OTHER = "Other"


class AnimalCase(db.Model, TimestampMixin):
	__tablename__ = "animal_cases"

	id = db.Column(db.Integer, primary_key=True)
	case_code = db.Column(db.String(20), unique=True, nullable=False)
	reporter_name = db.Column(db.String(255), nullable=True)
	reporter_phone = db.Column(db.String(30), nullable=False)
	location = db.Column(db.String(255), nullable=False)
	latitude = db.Column(db.Float, nullable=True)
	longitude = db.Column(db.Float, nullable=True)
	animal_type = db.Column(db.Enum(AnimalType), nullable=False, default=AnimalType.OTHER)
	urgency = db.Column(db.String(20), nullable=False)  # Low/Medium/Critical
	media_url = db.Column(db.String(512), nullable=True)
	notes = db.Column(db.Text, nullable=True)
	status = db.Column(db.Enum(CaseStatus), nullable=False, default=CaseStatus.PENDING)

	ngo_id = db.Column(db.Integer, db.ForeignKey("ngos.id"), nullable=True)
	assigned_volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"), nullable=True)
	hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=True)

	ngo = db.relationship("NGO", back_populates="cases")
	assigned_volunteer = db.relationship("Volunteer", back_populates="assigned_cases")
	hospital = db.relationship("Hospital", back_populates="cases")


class Donation(db.Model, TimestampMixin):
	__tablename__ = "donations"

	id = db.Column(db.Integer, primary_key=True)
	donor_name = db.Column(db.String(255), nullable=True)
	donor_email = db.Column(db.String(255), nullable=True)
	amount = db.Column(db.Numeric(10, 2), nullable=False)
	currency = db.Column(db.String(10), default="INR", nullable=False)
	category = db.Column(db.String(50), nullable=False)  # Medical Aid, Food, Shelter
	payment_provider = db.Column(db.String(50), nullable=True)  # Razorpay/Stripe
	payment_id = db.Column(db.String(255), nullable=True, unique=True)
	receipt_url = db.Column(db.String(512), nullable=True)
	ngo_id = db.Column(db.Integer, db.ForeignKey("ngos.id"), nullable=True)

	ngo = db.relationship("NGO")
