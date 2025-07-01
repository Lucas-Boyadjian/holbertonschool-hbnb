#!/usr/bin/env python3
"""Base model class for all models in the HolbertonBnB application."""

from app import db
import uuid
from datetime import datetime
from flask import Flask


class BaseModel:
    """Base class for all models.

    Provides common attributes/methods for other classes:
    - Unique identifier
    - Creation timestamp
    - Last update timestamp
    """
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based
        on the provided dictionary.

        Args:
            data (dict): Dictionary containing attribute
            names and values to update
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
