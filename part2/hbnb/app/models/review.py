#!/usr/bin/env python3

from .basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text:
            raise ValueError("Invalid text")
        if not (1 <= rating <= 5):
            raise ValueError("Invalid rating")
        if not place:
            raise ValueError("Invalid place")
        if not user:
            raise ValueError("invalid user")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
    