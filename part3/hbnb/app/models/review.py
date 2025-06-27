#!/usr/bin/env python3
"""Review model for HolbertonBnB application."""

from .basemodel import BaseModel


class Review(BaseModel):
    """Represents a review for a place.

    Attributes:
        text (str): Content of the review
        rating (int): Rating given (1-5 stars)
        place (Place): Place being reviewed
        user (User): User who wrote the review
    """

    def __init__(self, text, rating, place, user):
        """Initialize a new Review.

        Args:
            text (str): Content of the review
            rating (int): Rating given (1-5 stars)
            place (Place): Place being reviewed
            user (User): User who wrote the review

        Raises:
            ValueError: If any parameters are invalid
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """Get the review text."""
        return self._text

    @text.setter
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

    @property
    def rating(self):
        """Get the review rating."""
        return self._rating

    @rating.setter
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

    @property
    def place(self):
        """Get the place being reviewed."""
        return self._place

    @place.setter
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

    @property
    def user(self):
        """Get the user who wrote the review."""
        return self._user

    @user.setter
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
