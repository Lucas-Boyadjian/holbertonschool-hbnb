#!/usr/bin/env python3

from .basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first name")
        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last name")
        if not email or '@' not in email:
            raise ValueError("Invalid email")

    def add_place(self, place):
        self.places.append(place)

    def update(self, data):
        if "first_name" in data:
            if not data["first_name"] or len(data["first_name"]) > 50:
                raise ValueError("Invalid first name")
            self.first_name = data["first_name"]
        if "last_name" in data:
            if not data["last_name"] or len(data["last_name"]) > 50:
                raise ValueError("Invalid last name")
            self.first_name = data["last_name"]
        if "email" in data:
            if not data["email"] or '@' not in data["email"]:
                raise ValueError("Invalid email")
            self.email = data["email"]

    def to_dict(self):
        data = {
            "id_user": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
        if self.places:
            data["places"] = self.places
        return data