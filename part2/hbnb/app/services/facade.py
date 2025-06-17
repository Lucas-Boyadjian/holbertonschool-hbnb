#!/usr/bin/env python3

from app.persistence.repository import InMemoryRepository
from app.models.place import Place
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass
   
    def create_place(self, place_data):
        required_fields = ['title', 'price', 'latitude', 'longitude', 'user_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError("Missing required field: {}".format(field))

        user = self.get_user_by_id(place_data["user_id"])
        if user is None:
            raise ValueError("Invalid user_id: user does not exist.")
            
        new_place = Place(id=str(uuid.uuid4()),
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=user)

        self.places[new_place.id] = new_place
        return new_place

    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        place = self.places.get(place_id)
        if not place:
            raise Exception("Place not found.")
        return place

    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        return list(self.places.values())

    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        place = self.get_place(place_id)
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
            else:
                raise Exception("Invalid attribute: {}".format(key))
        return place
    