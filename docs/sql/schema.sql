-- MySQL schema for ResQTrack
CREATE TABLE admins (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	password_hash VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	is_superadmin TINYINT(1) NOT NULL DEFAULT 0,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL
) ENGINE=InnoDB;

CREATE TABLE ngos (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	phone VARCHAR(30) NOT NULL,
	location VARCHAR(255),
	operating_zones TEXT,
	approved TINYINT(1) NOT NULL DEFAULT 0,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL
) ENGINE=InnoDB;

CREATE TABLE volunteers (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	phone VARCHAR(30) NOT NULL,
	location VARCHAR(255),
	expertise VARCHAR(255),
	availability VARCHAR(255),
	approved TINYINT(1) NOT NULL DEFAULT 0,
	ngo_id INT,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
	CONSTRAINT fk_volunteer_ngo FOREIGN KEY (ngo_id) REFERENCES ngos(id)
) ENGINE=InnoDB;

CREATE TABLE hospitals (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	address VARCHAR(255),
	phone VARCHAR(30),
	location VARCHAR(255),
	is_24x7 TINYINT(1) NOT NULL DEFAULT 0,
	treatment_types VARCHAR(255),
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL
) ENGINE=InnoDB;

CREATE TABLE animal_cases (
	id INT AUTO_INCREMENT PRIMARY KEY,
	case_code VARCHAR(20) NOT NULL UNIQUE,
	reporter_name VARCHAR(255),
	reporter_phone VARCHAR(30) NOT NULL,
	location VARCHAR(255) NOT NULL,
	latitude DOUBLE,
	longitude DOUBLE,
	animal_type ENUM('Dog','Cat','Bird','Other') NOT NULL DEFAULT 'Other',
	urgency VARCHAR(20) NOT NULL,
	media_url VARCHAR(512),
	notes TEXT,
	status ENUM('PENDING','IN_PROGRESS','RESCUED','CLOSED') NOT NULL DEFAULT 'PENDING',
	ngo_id INT,
	assigned_volunteer_id INT,
	hospital_id INT,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
	CONSTRAINT fk_case_ngo FOREIGN KEY (ngo_id) REFERENCES ngos(id),
	CONSTRAINT fk_case_vol FOREIGN KEY (assigned_volunteer_id) REFERENCES volunteers(id),
	CONSTRAINT fk_case_hosp FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
) ENGINE=InnoDB;

CREATE TABLE donations (
	id INT AUTO_INCREMENT PRIMARY KEY,
	donor_name VARCHAR(255),
	donor_email VARCHAR(255),
	amount DECIMAL(10,2) NOT NULL,
	currency VARCHAR(10) NOT NULL DEFAULT 'INR',
	category VARCHAR(50) NOT NULL,
	payment_provider VARCHAR(50),
	payment_id VARCHAR(255) UNIQUE,
	receipt_url VARCHAR(512),
	ngo_id INT,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
	CONSTRAINT fk_donation_ngo FOREIGN KEY (ngo_id) REFERENCES ngos(id)
) ENGINE=InnoDB;
