from flask import Blueprint, request
from ..extensions import db
from ..models import Donation
from ..mailer import send_donation_receipt


donations_bp = Blueprint("donations", __name__, url_prefix="/donations")


@donations_bp.post("")
def create_donation():
	data = request.get_json(silent=True) or {}
	amount = data.get("amount")
	category = (data.get("category") or "").strip()
	if amount is None or not category:
		return {"error": "amount and category required"}, 400

	donation = Donation(
		donor_name=data.get("donor_name"),
		donor_email=data.get("donor_email"),
		amount=amount,
		currency=(data.get("currency") or "INR").upper(),
		category=category,
		payment_provider=data.get("payment_provider"),
		payment_id=data.get("payment_id"),
		ngo_id=data.get("ngo_id"),
	)
	db.session.add(donation)
	db.session.commit()

	try:
		if donation.donor_email:
			send_donation_receipt(donation.donor_email, str(donation.amount), donation.currency, donation.id)
	except Exception:
		pass

	return {"message": "Donation recorded", "id": donation.id}, 201
