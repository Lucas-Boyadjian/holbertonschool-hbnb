#!/usr/bin/env python3

from .basemodel import BaseModel
from app import db, bcrypt
import uuid
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String
from app.models.place import place_amenity

class Amenity(BaseModel):

    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("invalid name")
        return value    
    def to_dict(self,):
        return {
            "id": self.id,
            "name": self.name,
        }
