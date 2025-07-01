#!/usr/bin/env python3

from .basemodel import BaseModel
from app import db, bcrypt
import uuid
from sqlalchemy.orm import validates

class Amenity(BaseModel):

    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)


    @validates('name')
    def name(self, value):
        if not value or len(value) > 50:
            raise ValueError("invalid name")
        self._name = value    
    def to_dict(self,):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
