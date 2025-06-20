#!/usr/bin/env python3
"""Place model for HolbertonBnB application."""

from .basemodel import BaseModel


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

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialize a new Place.

        Args:
            title (str): The name/title of the place
            description (str): Description of the place
            price (float): Cost per night
            latitude (float): Geographic latitude
            longitude (float): Geographic longitude
            owner (User): User who owns the place

        Raises:
            ValueError: If any parameters are invalid
        """
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
    def title(self):
        """Get the title of the place."""
        return self._title

    @title.setter
    def title(self, value):
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
        self._title = value

    @property
    def price(self):
        """Get the price per night."""
        return self._price

    @price.setter
    def price(self, value):
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
        self._price = price_float

    @property
    def latitude(self):
        """Get the geographic latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
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
        self._latitude = latitude_float

    @property
    def longitude(self):
        """Get the geographic longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
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
        self._longitude = longitude_float
