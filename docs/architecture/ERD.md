# ER Diagram (Textual)

Entities and relationships:

- Admin (id, email, password_hash, name, is_superadmin)
- NGO (id, name, email, phone, location, operating_zones, approved)
  - has many Volunteers
  - has many AnimalCases
- Volunteer (id, name, email, phone, location, expertise, availability, approved, ngo_id)
  - belongs to NGO (optional)
  - has many assigned AnimalCases
- Hospital (id, name, address, phone, location, is_24x7, treatment_types)
  - has many AnimalCases
- AnimalCase (id, case_code, reporter_name, reporter_phone, location, latitude, longitude, animal_type, urgency, media_url, notes, status, ngo_id, assigned_volunteer_id, hospital_id)
  - belongs to NGO (optional)
  - belongs to Volunteer (optional)
  - belongs to Hospital (optional)
- Donation (id, donor_name, donor_email, amount, currency, category, payment_provider, payment_id, receipt_url, ngo_id)
  - belongs to NGO (optional)

Status enums:
- CaseStatus: PENDING, IN_PROGRESS, RESCUED, CLOSED
- AnimalType: Dog, Cat, Bird, Other
