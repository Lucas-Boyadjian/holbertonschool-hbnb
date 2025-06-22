#!/usr/bin/env python3
"""Tests for Place model and APIs."""

import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestPlaceModel(unittest.TestCase):
    """Test cases for Place model."""

    def test_place_creation(self):
        """Test successful Place creation with valid data."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")

        place = Place(title="Cozy Apartment",
                      description="A nice place to stay",
                      price=100, latitude=37.7749,
                      longitude=-122.4194, owner=owner)

        review = Review(text="Great stay!", rating=5,
                        place=place, user=owner)

        place.add_review(review)

        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.description, "A nice place to stay")
        self.assertEqual(place.price, 100)
        self.assertEqual(place.latitude, 37.7749)
        self.assertEqual(place.longitude, -122.4194)
        self.assertEqual(place.owner.first_name, "Alice")
        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Great stay!")
        self.assertEqual(place.reviews[0].rating, 5)

    def test_place_creation_empty_title(self):
        """Test that Place creation raises ValueError with empty title."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            Place(title="", description="A nice place to stay",
                  price=100, latitude=37.7749,
                  longitude=-122.4194, owner=owner)

    def test_place_creation_invalid_price_negative(self):
        """Test that Place creation raises ValueError with negative price."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment",
                  description="A nice place to stay",
                  price=-50, latitude=37.7749,
                  longitude=-122.4194, owner=owner)

    def test_place_creation_invalid_price_string(self):
        """Test that Place creation raises ValueError
            with non-numeric price."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay",
                  price="not-a-price",
                  latitude=37.7749, longitude=-122.4194, owner=owner)

    def test_place_creation_invalid_latitude_high(self):
        """Test that Place creation raises ValueError with latitude > 90."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay",
                  price=100, latitude=95, longitude=-122.4194, owner=owner)

    def test_place_creation_invalid_latitude_low(self):
        """Test that Place creation raises ValueError with latitude < -90."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay",
                  price=100, latitude=-95, longitude=-122.4194, owner=owner)

    def test_place_creation_invalid_longitude_high(self):
        """Test that Place creation raises ValueError with longitude > 180."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay",
                  price=100, latitude=37.7749, longitude=185, owner=owner)

    def test_place_creation_invalid_longitude_low(self):
        """Test that Place creation raises ValueError with longitude < -180."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay",
                  price=100, latitude=37.7749, longitude=-185, owner=owner)

    def test_place_creation_null_owner(self):
        """Test that Place creation raises ValueError with null owner."""
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", description="A nice place to stay",
                  price=100, latitude=37.7749, longitude=-122.4194, owner=None)

    def test_place_amenities(self):
        """Test adding amenities to a place."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")

        place = Place(title="Cozy Apartment",
                      description="A nice place to stay",
                      price=100, latitude=37.7749,
                      longitude=-122.4194, owner=owner)

        wifi = Amenity(name="Wi-Fi")
        piscine = Amenity(name="Piscine")

        place.add_amenity(wifi)
        place.add_amenity(piscine)

        self.assertEqual(len(place.amenities), 2)
        self.assertEqual(place.amenities[0].name, "Wi-Fi")
        self.assertEqual(place.amenities[1].name, "Piscine")

    def test_place_multiple_reviews(self):
        """Test adding multiple reviews to a place."""
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")

        place = Place(title="Cozy Apartment",
                      description="A nice place to stay",
                      price=100, latitude=37.7749,
                      longitude=-122.4194, owner=owner)

        user1 = User(first_name="Bob", last_name="Johnson",
                     email="bob@example.com")
        user2 = User(first_name="Charlie", last_name="Brown",
                     email="charlie@example.com")

        review1 = Review(text="Great location!", rating=5,
                         place=place, user=user1)
        review2 = Review(text="Very clean", rating=4,
                         place=place, user=user2)

        place.add_review(review1)
        place.add_review(review2)

        self.assertEqual(len(place.reviews), 2)
        self.assertEqual(place.reviews[0].text, "Great location!")
        self.assertEqual(place.reviews[0].rating, 5)
        self.assertEqual(place.reviews[1].text, "Very clean")
        self.assertEqual(place.reviews[1].rating, 4)


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place API endpoints."""

    def setUp(self):
        """Set up test client and create a test user."""
        self.app = create_app()
        self.client = self.app.test_client()

        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        })
        self.user_id = response.json["id_user"]

    def test_create_place(self):
        """Test creating a place with valid data."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["title"], "Cozy Apartment")
        self.assertEqual(response.json["description"], "A nice place to stay")
        self.assertEqual(response.json["price"], 100)
        self.assertEqual(response.json["latitude"], 37.7749)
        self.assertEqual(response.json["longitude"], -122.4194)
        self.assertEqual(response.json["owner_id"], self.user_id)
        self.assertIn("id", response.json)

        self.place_id = response.json["id"]

    def test_create_place_empty_title(self):
        """Test that creating a place with empty title fails."""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_place_invalid_price(self):
        """Test that creating a place with negative price fails."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -50,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_place_invalid_latitude(self):
        """Test that creating a place with invalid latitude fails."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 95,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_place_invalid_longitude(self):
        """Test that creating a place with invalid longitude fails."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": 185,
            "owner_id": self.user_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_place_invalid_owner(self):
        """Test that creating a place with invalid owner_id fails."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "invalid-owner-id"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_get_all_places(self):
        """Test getting all places."""
        self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        response = self.client.get('/api/v1/places/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    def test_get_place_by_id(self):
        """Test getting a specific place by ID."""
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        place_id = create_response.json["id"]

        response = self.client.get('/api/v1/places/{}'.format(place_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], place_id)
        self.assertEqual(response.json["title"], "Cozy Apartment")
        self.assertEqual(response.json["description"], "A nice place to stay")
        self.assertEqual(response.json["price"], 100)

    def test_get_places_by_owner(self):
        """Test getting all places for a specific owner."""
        self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "Relaxing beach getaway",
            "price": 150,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": self.user_id
        })

        response = self.client.get('/api/v1/users/{}/places'.format(self.user_id))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 2)

        for place in response.json:
            self.assertEqual(place["owner_id"], self.user_id)

    def test_get_nonexistent_place(self):
        """Test getting a place that doesn't exist."""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)

    def test_update_place(self):
        """Test updating a place's attributes."""
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        place_id = create_response.json["id"]

        update_response = self.client.put('/api/v1/places/{}'.format(place_id), json={
            "title": "Luxury Apartment",
            "description": "An upgraded place to stay",
            "price": 150
        })

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["title"], "Luxury Apartment")
        self.assertEqual(update_response.json["description"],
                         "An upgraded place to stay")
        self.assertEqual(update_response.json["price"], 150)

        self.assertEqual(update_response.json["latitude"], 37.7749)
        self.assertEqual(update_response.json["longitude"], -122.4194)

    def test_update_place_invalid_data(self):
        """Test updating a place with invalid data."""
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })

        place_id = create_response.json["id"]

        update_response = self.client.put('/api/v1/places/{}'.format(place_id), json={
            "title": "",
            "price": -50
        })

        self.assertEqual(update_response.status_code, 400)
        self.assertIn("error", update_response.json)

if __name__ == '__main__':
    unittest.main()
