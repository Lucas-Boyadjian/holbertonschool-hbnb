#!/usr/bin/env python3

from .basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
    @property
    def name(self):
        return self._name
    
    @name.setter
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
