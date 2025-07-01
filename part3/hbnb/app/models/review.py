#!/usr/bin/env python3
"""Review model for HolbertonBnB application."""

from .basemodel import BaseModel
from app import db, bcrypt
import uuid
from sqlalchemy.orm import validates


class Review(BaseModel):
    """Represents a review for a place.

    Attributes:
        text (str): Content of the review
        rating (int): Rating given (1-5 stars)
        place (Place): Place being reviewed
        user (User): User who wrote the review
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    text = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


    @validates('text')
    def text(self, value):
        """Set the review text.

        Args:
            value (str): New text for the review

        Raises:
            ValueError: If text is empty
        """
        if not value:
            raise ValueError("Invalid text")
        self._text = value

    
    @validates('rating')
    def rating(self, value):
        """Set the review rating.

        Args:
            value (int): New rating (1-5)

        Raises:
            ValueError: If rating is not between 1 and 5
        """
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Invalid rating")
        self._rating = value

    
    @validates('place')
    def place(self, value):
        """Set the place being reviewed.

        Args:
            value (Place): The place

        Raises:
            ValueError: If place is None
        """
        if not value:
            raise ValueError("Invalid place")
        self._place = value

    
    @validates('user')
    def user(self, value):
        """Set the user who wrote the review.

        Args:
            value (User): The user

        Raises:
            ValueError: If user is None
        """
        if not value:
            raise ValueError("Invalid user")
        self._user = value
