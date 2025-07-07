-- database: development.db
-- inserte data and create admin
-- and add 3 amenity

INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES ("36c9050e-ddd3-4c3b-9731-9f487208bbc1", "admin@hbnb.io", "Admin", "HBnB", "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBVpTS9vV5qHBe", true);

INSERT INTO amenities (id, name) VALUES 
("550e8400-e29b-41d4-a716-446655440001", "Wi-Fi"),
("550e8400-e29b-41d4-a716-446655440002", "Piscine"),
("550e8400-e29b-41d4-a716-446655440003", "Climatisation");