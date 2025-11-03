from backend.app.extensions import db
from backend.app.models import AnimalCase, CaseStatus


def test_public_case_creation(client):
	payload = {
		"reporter_phone": "9999999999",
		"location": "Test City",
		"animal_type": "Dog",
		"urgency": "Low",
		"notes": "test",
	}
	res = client.post("/cases", json=payload)
	assert res.status_code == 201
	data = res.get_json()
	assert data["case_id"]

	case = AnimalCase.query.get(data["case_id"])
	assert case.status == CaseStatus.PENDING
