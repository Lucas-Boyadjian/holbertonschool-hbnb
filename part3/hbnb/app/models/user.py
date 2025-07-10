#!/usr/bin/env python3

from app import db, bcrypt
import uuid
from sqlalchemy.orm import validates, relationship, backref
from .basemodel import BaseModel
from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    places = relationship('Place', backref='user', lazy=True)
    reviews = relationship('Review', backref='user', lazy=True)
    
    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Invalid first name")
        return value
    
    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Invalid last name")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value or '@' not in value:
            raise ValueError("Invalid email")
        return value

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