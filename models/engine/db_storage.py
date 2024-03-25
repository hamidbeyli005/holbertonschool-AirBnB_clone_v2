#!/usr/bin/python3

from models.base_model import BaseModel, Base
import os
from sqlalchemy import create_engine

class DBStorage(Base):
    __engine = None
    __session = None
    
    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST'),
                                             os.getenv('HBNB_MYSQL_DB'),
                                             pool_pre_ping=True))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """ Returns a dictionary of models currently in storage """
        from models import storage
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        from models import classes
        if cls:
            objects = self.__session.query(classes[cls]).all()
        else:
            objects = []
            for key, value in classes.items():
                objects += self.__session.query(value).all()
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objects}
    
    def new(self, obj):
        """ Adds new object to storage dictionary """
        self.__session.add(obj)
    
    def save(self):
        """ Saves storage dictionary to file """
        self.__session.commit()
    
    def delete(self, obj=None):
        """ Deletes obj from objects """
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        """ Loads storage dictionary from file """
        from sqlalchemy.orm import sessionmaker, scoped_session
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)