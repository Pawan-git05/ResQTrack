# Data Flow Diagram (DFD) - Level 1 (Textual)

Actors: Citizen, Volunteer, NGO Admin, Hospital Staff, Payment Gateway

Flows:
1. Citizen -> Report Form -> API (/cases) -> DB (AnimalCase) -> Email Confirmation
2. NGO Admin -> Auth -> Dashboard -> Assign Volunteer -> DB (AnimalCase updates)
3. Volunteer -> Auth -> Case Update (/cases/:id/status) -> DB
4. Hospital Staff -> Directory Registration -> DB (Hospital)
5. Donor -> Donate Form -> API (/donations) -> Payment Provider (future) -> DB -> Email Receipt

Data Stores:
- MySQL: NGOs, Volunteers, AnimalCases, Hospitals, Donations, Admins
- Uploads: media files (local or S3)
