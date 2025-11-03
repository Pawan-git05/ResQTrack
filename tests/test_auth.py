from backend.app.extensions import db
from backend.app.models import Admin
from backend.app.utils import hash_password


def test_login_and_protected_flow(client):
	# Seed admin
	admin = Admin(email="admin@example.com", name="Admin", password_hash=hash_password("secret"))
	db.session.add(admin)
	db.session.commit()

	# Login
	res = client.post("/auth/login", json={"email": "admin@example.com", "password": "secret", "role": "ADMIN"})
	assert res.status_code == 200
	token = res.get_json()["access_token"]
	assert token

	# Access a protected endpoint (update case status requires jwt but we need a case id; expect 404, not 401)
	r = client.patch("/cases/999/status", json={"status": "CLOSED"}, headers={"Authorization": f"Bearer {token}"})
	assert r.status_code in (404, 400)
