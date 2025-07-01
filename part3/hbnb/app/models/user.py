#!/usr/bin/env python3

from app import db, bcrypt
import uuid
from sqlalchemy.orm import validates
from .basemodel import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    @validates('first_name')
    def validate_first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Invalid first name")
        self._first_name = value
    
    @validates('last_name')
    def validate_last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Invalid last name")
        self._last_name = value

    @validates('email')
    def validate_email(self, value):
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
            "email": self.email
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