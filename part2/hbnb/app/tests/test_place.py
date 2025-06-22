#!/usr/bin/env python3
"""Tests for Place model and APIs."""

import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


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
        self.assertEqual("id" in response.json, True)

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
        self.assertEqual("error" in response.json, True)

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
        self.assertEqual("error" in response.json, True)

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
        self.assertEqual("error" in response.json, True)

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
        self.assertEqual("error" in response.json, True)

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
        self.assertEqual("error" in response.json, True)

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
        self.assertEqual(isinstance(response.json, list), True)
        self.assertEqual(len(response.json) > 0, True)

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

        response = self.client.get('/api/v1/users/{}/places'
                                   .format(self.user_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(isinstance(response.json, list), True)
        self.assertEqual(len(response.json) >= 2, True)

        for place in response.json:
            self.assertEqual(place["owner_id"], self.user_id)

    def test_get_nonexistent_place(self):
        """Test getting a place that doesn't exist."""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual("error" in response.json, True)

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

        update_response = self.client.put(
            '/api/v1/places/{}'.format(place_id),
            json={
                "title": "Luxury Apartment",
                "description": "An upgraded place to stay",
                "price": 150
            }
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["title"], "Luxury Apartment")
        self.assertEqual(
            update_response.json["description"],
            "An upgraded place to stay"
        )
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

        update_response = self.client.put(
            '/api/v1/places/{}'.format(place_id),
            json={
                "title": "",
                "price": -50
            }
        )

        self.assertEqual(update_response.status_code, 400)
        self.assertEqual("error" in update_response.json, True)


if __name__ == '__main__':
    unittest.main()
