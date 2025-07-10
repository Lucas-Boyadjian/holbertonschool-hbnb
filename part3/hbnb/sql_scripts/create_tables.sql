-- this file is a script, that create
-- tables structures 

CREATE TABLE users (
	id CHAR(36) PRIMARY KEY,
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	email VARCHAR(255) UNIQUE,
	password VARCHAR(255),
	is_admin BOOLEAN DEFAULT FALSE,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE places (
	id CHAR(36) PRIMARY KEY,
	title VARCHAR(255),
	description TEXT,
	price DECIMAL(10, 2),
	latitude FLOAT,
	longitude FLOAT,
	owner_id CHAR(36),
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (owner_id) REFERENCES users(id)
);


CREATE TABLE reviews (
	   id CHAR(36) PRIMARY KEY,
	   text TEXT,
	   rating INT CHECK (rating >= 1 AND rating <= 5),
	   user_id CHAR(36),
	   place_id CHAR(36),
	   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	   updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	   UNIQUE (user_id, place_id),
	   FOREIGN KEY (user_id) REFERENCES users(id),
	   FOREIGN KEY (place_id) REFERENCES places(id)
);

CREATE TABLE amenities (
	id CHAR(36) PRIMARY KEY,
	name VARCHAR(255) UNIQUE,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE place_amenity (
	   place_id CHAR(36),
	   amenity_id CHAR(36),
	   PRIMARY KEY (place_id, amenity_id),
	   FOREIGN KEY (place_id) REFERENCES places(id),
	   FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);