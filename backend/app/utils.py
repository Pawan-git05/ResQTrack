import random
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password: str) -> str:
	return generate_password_hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
	return check_password_hash(password_hash, plain_password)


def generate_case_code(prefix: str = "A") -> str:
	stamp = datetime.utcnow().strftime("%y%m%d%H%M%S")
	rand = "".join(random.choices(string.digits, k=3))
	return f"{prefix}{stamp}{rand}"
