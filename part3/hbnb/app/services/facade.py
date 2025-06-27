#!/usr/bin/env python3

from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)  # Switched to SQLAlchemyRepository
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()
    
    def put_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(data)
        return user
   
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
                        raise ValueError("Amenity with id {} does not exist.".format(amenity_id))
                    place.add_amenity(amenity)
    
        return place
    
    def create_review(self, review_data):
        """Create a new review with validation"""
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")
    
        rating = review_data['rating']
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
    
        user = self.user_repo.get(review_data['user_id'])
        if user is None:
            raise ValueError(f"User with id {review_data['user_id']} does not exist.")
    
        place = self.place_repo.get(review_data['place_id'])
        if place is None:
            raise ValueError(f"Place with id {review_data['place_id']} does not exist.")
    
        from app.models.review import Review
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
    
        self.review_repo.add(new_review)
    
        place.add_review(new_review)
    
        return new_review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        review = self.review_repo.get(review_id)
        if review is None:
            raise KeyError("Review not found.")
        return review

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if place is None:
            raise KeyError("Place not found.")
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.get_review(review_id)
    
        if 'text' in review_data:
            review.text = review_data['text']
    
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating
    
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.get_review(review_id)
    
        if hasattr(review, 'place') and review.place:
            if review in review.place.reviews:
                review.place.reviews.remove(review)
    
        self.review_repo.delete(review_id)
    
        return True