#!/usr/bin/env python3

from .basemodel import BaseModel
import datetime

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Invalid name")
        self.name = name
    
    def to_dict(self,):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    def update(self, data):
        if "name" in data:
            if not data["name"] or len(data["name"]) > 50:
                raise ValueError("Invalid name")
            self.name = data["name"]
        self.updated_at = datetime.datetime.now()