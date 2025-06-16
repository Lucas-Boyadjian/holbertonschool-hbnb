from basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Invalid title")
        if not price or price < 0:
            raise ValueError("Invalid price")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Invalid latitude")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Invalid longitude")
        if not owner:
            raise ValueError("Invalid owner")
                
        self.title = title
        self.descrption = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)