-- Enhanced Sample Data for ResQTrack Database
-- This script inserts comprehensive sample data for hospitals, NGOs, reports (animal cases), and volunteers

-- Insert Admins
INSERT INTO admins (name, email, password_hash, is_superadmin, created_at, updated_at)
VALUES
('Super Admin', 'admin@resqtrack.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj5q7VqVjK4K', 1, NOW(), NOW()),
('John Doe', 'john@resqtrack.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj5q7VqVjK4K', 0, NOW(), NOW());

-- Insert NGOs
INSERT INTO ngos (name, email, phone, location, operating_zones, approved, created_at, updated_at)
VALUES
('Paws Care Foundation', 'contact@pawscare.org', '9999999999', 'City Center', 'Sector 1, Sector 2, Sector 3', 1, NOW(), NOW()),
('Animal Rescue Society', 'info@animalrescue.org', '8888888888', 'Suburb Area', 'Sector 4, Sector 5', 1, NOW(), NOW()),
('Street Animals Help', 'help@streetanimals.org', '7777777777', 'Downtown', 'Sector 6, Sector 7', 0, NOW(), NOW()),
('Wildlife Protection NGO', 'wildlife@protection.org', '6666666666', 'Forest Area', 'Rural Areas, Forest Zones', 1, NOW(), NOW()),
('Pet Care Community', 'community@petcare.org', '5555555555', 'Residential Area', 'Sector 8, Sector 9', 1, NOW(), NOW());

-- Insert Volunteers
INSERT INTO volunteers (name, email, phone, location, expertise, availability, approved, ngo_id, created_at, updated_at)
VALUES
('Riya Sharma', 'riya@example.com', '8888888888', 'Sector 1', 'Pickup, First Aid', 'Evenings, Weekends', 1, 1, NOW(), NOW()),
('Amit Kumar', 'amit@example.com', '7777777777', 'Sector 2', 'Transportation', 'Mornings, Afternoons', 1, 1, NOW(), NOW()),
('Priya Singh', 'priya@example.com', '6666666666', 'Sector 4', 'Foster Care', 'Flexible', 1, 2, NOW(), NOW()),
('Raj Patel', 'raj@example.com', '5555555555', 'Sector 5', 'Emergency Response', '24/7', 1, 2, NOW(), NOW()),
('Sneha Gupta', 'sneha@example.com', '4444444444', 'Sector 6', 'Medical Care', 'Weekdays', 0, 3, NOW(), NOW()),
('Arjun Mehta', 'arjun@example.com', '3333333333', 'Sector 8', 'Wildlife Rescue', 'Weekends', 1, 4, NOW(), NOW()),
('Kavya Reddy', 'kavya@example.com', '2222222222', 'Sector 9', 'Pet Care', 'Evenings', 1, 5, NOW(), NOW()),
('Rohit Sharma', 'rohit@example.com', '1111111111', 'Sector 3', 'Training', 'Flexible', 1, 1, NOW(), NOW());

-- Insert Hospitals
INSERT INTO hospitals (name, address, phone, location, is_24x7, treatment_types, created_at, updated_at)
VALUES
('City Veterinary Clinic', '123 Main Road, City Center', '9999999999', 'Sector 15', 1, 'Surgery, First Aid, Emergency Care', NOW(), NOW()),
('Animal Care Hospital', '456 Park Avenue, Suburb', '8888888888', 'Sector 20', 0, 'General Treatment, Vaccination', NOW(), NOW()),
('Emergency Pet Clinic', '789 Emergency Lane, Downtown', '7777777777', 'Sector 25', 1, 'Emergency Surgery, Critical Care', NOW(), NOW()),
('Wildlife Rehabilitation Center', '321 Forest Road, Rural Area', '6666666666', 'Forest Zone', 0, 'Wildlife Care, Rehabilitation', NOW(), NOW()),
('Pet Wellness Center', '654 Health Street, Residential', '5555555555', 'Sector 30', 0, 'Wellness Checkups, Vaccination', NOW(), NOW()),
('Critical Care Animal Hospital', '987 Emergency Blvd, City', '4444444444', 'Sector 35', 1, 'ICU, Surgery, Emergency', NOW(), NOW());

-- Insert Animal Cases (Reports)
INSERT INTO animal_cases (case_code, reporter_name, reporter_phone, location, latitude, longitude, animal_type, urgency, notes, status, ngo_id, assigned_volunteer_id, hospital_id, created_at, updated_at)
VALUES
('A250101120000123', 'Amit Kumar', '9000000000', 'Sector 15, Near Park', 28.6139, 77.2090, 'Dog', 'Medium', 'Injured dog found near the park. Seems to have a leg injury.', 'PENDING', 1, 1, 1, NOW(), NOW()),
('A250101120000124', 'Priya Singh', '8000000000', 'Sector 20, Street Corner', 28.6140, 77.2091, 'Cat', 'Critical', 'Cat stuck in drain pipe. Needs immediate rescue.', 'IN_PROGRESS', 2, 3, 2, NOW(), NOW()),
('A250101120000125', 'Raj Patel', '7000000000', 'Sector 25, Construction Site', 28.6141, 77.2092, 'Bird', 'Low', 'Bird with broken wing found at construction site.', 'RESCUED', 1, 2, 3, NOW(), NOW()),
('A250101120000126', 'Sneha Gupta', '6000000000', 'Forest Area, Near Highway', 28.6142, 77.2093, 'Other', 'Medium', 'Deer found injured near highway. Wildlife rescue needed.', 'PENDING', 4, 6, 4, NOW(), NOW()),
('A250101120000127', 'Anonymous', '5000000000', 'Sector 10, Residential Area', 28.6143, 77.2094, 'Dog', 'Critical', 'Dog hit by vehicle. Bleeding heavily. Emergency required.', 'IN_PROGRESS', 1, 4, 1, NOW(), NOW()),
('A250101120000128', 'Vikram Singh', '4000000000', 'Sector 8, Near School', 28.6144, 77.2095, 'Cat', 'Medium', 'Stray cat with skin infection. Needs medical attention.', 'PENDING', 5, 7, 5, NOW(), NOW()),
('A250101120000129', 'Anita Patel', '3000000000', 'Sector 30, Market Area', 28.6145, 77.2096, 'Dog', 'Low', 'Puppy found abandoned. Looking for foster care.', 'RESCUED', 2, 4, 2, NOW(), NOW()),
('A250101120000130', 'Rohit Kumar', '2000000000', 'Sector 35, Industrial Area', 28.6146, 77.2097, 'Bird', 'Critical', 'Eagle with injured wing. Wildlife rescue required.', 'IN_PROGRESS', 4, 6, 6, NOW(), NOW()),
('A250101120000131', 'Meera Sharma', '1000000000', 'Sector 9, Residential Complex', 28.6147, 77.2098, 'Cat', 'Medium', 'Cat with eye infection. Needs veterinary care.', 'PENDING', 3, 5, 3, NOW(), NOW()),
('A250101120000132', 'Anonymous', '9000000001', 'Sector 12, Park Area', 28.6148, 77.2099, 'Dog', 'Low', 'Healthy stray dog. Needs vaccination and neutering.', 'PENDING', 1, 8, 1, NOW(), NOW());

-- Insert Donations
INSERT INTO donations (donor_name, donor_email, amount, currency, category, payment_provider, payment_id, ngo_id, created_at, updated_at)
VALUES
('Neha Sharma', 'neha@example.com', 500.00, 'INR', 'Medical Aid', 'Razorpay', 'pay_123456789', 1, NOW(), NOW()),
('Vikram Singh', 'vikram@example.com', 1000.00, 'INR', 'Food Supplies', 'Razorpay', 'pay_123456790', 2, NOW(), NOW()),
('Anita Patel', 'anita@example.com', 2500.00, 'INR', 'Shelter', 'Razorpay', 'pay_123456791', 1, NOW(), NOW()),
('Rohit Kumar', 'rohit@example.com', 750.00, 'INR', 'Emergency Fund', 'Razorpay', 'pay_123456792', 4, NOW(), NOW()),
('Anonymous', NULL, 200.00, 'INR', 'General', 'Razorpay', 'pay_123456793', 3, NOW(), NOW()),
('Priya Reddy', 'priya@example.com', 1500.00, 'INR', 'Medical Equipment', 'Razorpay', 'pay_123456794', 5, NOW(), NOW()),
('Arjun Mehta', 'arjun@example.com', 800.00, 'INR', 'Transportation', 'Razorpay', 'pay_123456795', 2, NOW(), NOW()),
('Kavya Singh', 'kavya@example.com', 3000.00, 'INR', 'Infrastructure', 'Razorpay', 'pay_123456796', 1, NOW(), NOW()),
('Ravi Kumar', 'ravi@example.com', 600.00, 'INR', 'Food Supplies', 'Razorpay', 'pay_123456797', 4, NOW(), NOW()),
('Anonymous', NULL, 1200.00, 'INR', 'Emergency Fund', 'Razorpay', 'pay_123456798', 5, NOW(), NOW());

-- Display summary
SELECT 'Sample data insertion completed!' as Status;
SELECT COUNT(*) as Total_NGOs FROM ngos;
SELECT COUNT(*) as Total_Volunteers FROM volunteers;
SELECT COUNT(*) as Total_Hospitals FROM hospitals;
SELECT COUNT(*) as Total_Animal_Cases FROM animal_cases;
SELECT COUNT(*) as Total_Donations FROM donations;
SELECT COUNT(*) as Total_Admins FROM admins;
