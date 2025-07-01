#!/usr/bin/env python3
"""Place model for HolbertonBnB application."""

from .basemodel import BaseModel
from app import db, bcrypt
import uuid
from sqlalchemy.orm import validates


class Place(BaseModel):
    """Represents a rental property in the application.

    Attributes:
        title (str): The name/title of the place
        description (str): Detailed description of the place
        price (float): Cost per night to rent the place
        latitude (float): Geographic latitude of the place (-90 to 90)
        longitude (float): Geographic longitude of the place (-180 to 180)
        owner (User): User who owns the place
        reviews (list): List of Review objects for this place
        amenities (list): List of Amenity objects for this place
    """
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @validates('title')
    def title(self, key, value):
        """Set the title of the place.

        Args:
            value (str): New title for the place

        Raises:
            ValueError: If title is empty or too long
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title cannot be None.")
        if len(value) > 100:
            raise ValueError("Title must be 100 characters max.")
        return value


    @validates('price')
    def price(self, key, value):
        """Set the price per night.

        Args:
            value (float): New price

        Raises:
            ValueError: If price is negative or not a number
        """
        if value is None:
            raise ValueError("Price cannot be None")
        try:
            price_float = float(value)
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number")
        if price_float < 0:
            raise ValueError("Price cannot be negative")
        return price_float

    
    @validates('latitude')
    def latitude(self, key, value):
        """Set the geographic latitude.

        Args:
            value (float): New latitude

        Raises:
            ValueError: If latitude is not between -90 and 90
        """
        if value is None:
            raise ValueError("Latitude cannot be None")
        try:
            latitude_float = float(value)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a valid number")
        if not (-90.0 <= latitude_float <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        return latitude_float

   
    @validates('longitude')
    def longitude(self, key, value):
        """Set the geographic longitude.

        Args:
            value (float): New longitude

        Raises:
            ValueError: If longitude is not between -180 and 180
        """
        if value is None:
            raise ValueError("Longitude cannot be None")
        try:
            longitude_float = float(value)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a valid number")
        if not (-180.0 <= longitude_float <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return longitude_float
