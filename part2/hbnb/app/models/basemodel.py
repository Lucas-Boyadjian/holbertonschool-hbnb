#!/usr/bin/env python3
"""Base model class for all models in the HolbertonBnB application."""

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

    def __init__(self):
        """Initialize a new BaseModel instance.

        Sets up:
        - A unique id using UUID4
        - Creation timestamp
        - Last update timestamp (initially same as creation)
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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
