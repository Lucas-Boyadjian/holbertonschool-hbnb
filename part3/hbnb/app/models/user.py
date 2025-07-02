#!/usr/bin/env python3

from .basemodel import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    def __init__(self, first_name, last_name, email, hash_password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.password = hash_password

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Invalid first name")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Invalid last name")
        self._last_name = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value or '@' not in value:
            raise ValueError("Invalid email")
        self._email = value

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
            self.last_name = data["last_name"]
        if "email" in data:
            if not data["email"] or '@' not in data["email"]:
                raise ValueError("Invalid email")
            self.email = data["email"]

    def to_dict(self):
        data = {
            "id_user": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
        if self.places:
            data["places"] = self.places
        return data
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)