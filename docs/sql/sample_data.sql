INSERT INTO ngos (name, email, phone, location, operating_zones, approved, created_at, updated_at)
VALUES
('Paws Care', 'contact@pawscare.org', '9999999999', 'City Center', 'Sector 1, Sector 2', 1, NOW(), NOW());

INSERT INTO volunteers (name, email, phone, expertise, availability, approved, ngo_id, created_at, updated_at)
VALUES
('Riya', 'riya@example.com', '8888888888', 'Pickup', 'Evenings', 1, 1, NOW(), NOW());

INSERT INTO hospitals (name, address, phone, location, is_24x7, treatment_types, created_at, updated_at)
VALUES
('City Vet Clinic', 'Main Road', '7777777777', 'Sector 15', 1, 'Surgery, First Aid', NOW(), NOW());

INSERT INTO animal_cases (case_code, reporter_name, reporter_phone, location, animal_type, urgency, status, created_at, updated_at)
VALUES
('A250101120000123', 'Amit', '9000000000', 'Sector 15', 'Dog', 'Medium', 'PENDING', NOW(), NOW());

INSERT INTO donations (donor_name, donor_email, amount, currency, category, created_at, updated_at)
VALUES
('Neha', 'neha@example.com', 500.00, 'INR', 'Medical Aid', NOW(), NOW());
