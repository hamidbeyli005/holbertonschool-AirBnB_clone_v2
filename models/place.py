#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel,Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.engine.file_storage import FileStorage


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    # user = relationship("User", back_populates="places")
    # city = relationship("City", back_populates="places", foreign_keys=[city_id])
    reviews = relationship("Review", backref="place", cascade="all, delete")
    place_amenity = Table('place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
    )
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    @property
    def reviews(self):
        storage = FileStorage()
        return [review for review in storage.all(Review).values()
                if review.place_id == self.id]

    @property
    def amenities(self):
        storage = FileStorage()
        return [storage.get(Amenity, amenity_id) for amenity_id in self.amenity_ids]

    @amenities.setter
    def amenities(self, amenity):
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
