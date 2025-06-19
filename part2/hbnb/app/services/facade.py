#!/usr/bin/env python3

from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_user(self):
        return self.user_repo.get_all()
    
    def put_user(self, user_id, data):
        return self.user_repo.update(user_id, data)
   
    def get_all_user(self):
        return self.user_repo.get_all()

    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        new_amenity = Amenity(name)
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        new_amenity = self.amenity_repo.get(amenity_id)
        return new_amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity is None:
            return None
        amenity.update(amenity_data)
        return amenity

    
    def create_place(self, place_data):
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError("Missing required field: {}".format(field))

        owner = self.get_user(place_data["owner_id"])
        if owner is None:
            raise ValueError("Invalid owner_id: owner does not exist.")
    
        new_place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

        amenities = place_data.get('amenities', [])
    
        for amenity_item in amenities:
            if isinstance(amenity_item, dict):
                amenity_id = amenity_item.get('id')
            elif isinstance(amenity_item, str):
                amenity_id = amenity_item
            else:
                continue
            
            if amenity_id:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity is None:
                    raise ValueError("Amenity with id {} does not exist.".format(amenity_id))
                new_place.add_amenity(amenity)

        self.place_repo.add(new_place)
        owner.add_place(new_place)
        return new_place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place is None:
            raise KeyError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place with the given data"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place with id {} does not exist.".format(place_id))
    
        updatable_attrs = ['title', 'description', 'price', 'latitude', 'longitude']
        for attr in updatable_attrs:
            if attr in place_data and place_data[attr] is not None:
                setattr(place, attr, place_data[attr])
    
        if 'amenities' in place_data:
            place.amenities = []
        
            for amenity_item in place_data['amenities']:
                if isinstance(amenity_item, dict):
                    amenity_id = amenity_item.get('id')
                elif isinstance(amenity_item, str):
                    amenity_id = amenity_item
                else:
                    continue
                
                if amenity_id:
                    amenity = self.amenity_repo.get(amenity_id)
                    if amenity is None:
                        raise ValueError("Amenity with id {amenity_id} does not exist.".format(amenity_id))
                    place.add_amenity(amenity)
    
        return place
        
    
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
    # Placeholder for logic to delete a review
        pass
