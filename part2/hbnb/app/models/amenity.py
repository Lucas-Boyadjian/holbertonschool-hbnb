#!/usr/bin/env python3

from .basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Invalid name")
        self.name = name