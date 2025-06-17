#!/usr/bin/env python3

from .basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not owner:
            raise ValueError("Invalid owner")
                
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value is None:
            raise ValueError("Price cannot be None")
        try:
            price_float = float(value)
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number")
        if price_float < 0:
            raise ValueError("Price cannot be negative")
        self._price = price_float

    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        if value is None:
            raise ValueError("Latitude cannot be None")
        try:
            latitude_float = float(value)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a valid number")
        if not (-90.0 <= latitude_float <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = latitude_float
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        if value is None:
            raise ValueError("Longitude cannot be None")
        try:
            longitude_float = float(value)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a valid number")
        if not (-180.0 <= longitude_float <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = longitude_float
