from flask_mail import Message
from flask import current_app
from .extensions import mail


def send_case_confirmation(to_email: str, case_code: str) -> None:
	if not to_email:
		return
	subject = f"ResQTrack: Case {case_code} Received"
	body = f"Thank you for reporting. Your case ID is {case_code}. Our team will coordinate shortly."
	msg = Message(subject=subject, recipients=[to_email], body=body)
	mail.send(msg)


def send_donation_receipt(to_email: str, amount: str, currency: str, donation_id: int) -> None:
	if not to_email:
		return
	subject = "ResQTrack: Donation Receipt"
	body = f"Thank you for your donation of {currency} {amount}. Receipt ID: {donation_id}."
	msg = Message(subject=subject, recipients=[to_email], body=body)
	mail.send(msg)
