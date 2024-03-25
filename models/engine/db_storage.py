#!/usr/bin/python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import models

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
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
        """ Returns a dictionary of objects """
        if cls:
            if isinstance(cls, str):
                cls = models.get(cls)
            return {obj.__class__.__name__ + "." + obj.id: obj for obj in self.__session.query(cls)}
        else:
            obj_dict = {}
            for cls in models.classes:
                obj_dict.update({obj.__class__.__name__ + "." + obj.id: obj for obj in self.__session.query(cls)})
            return obj_dict

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
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
