#!/usr/bin/python3
""" """
import unittest
from unittest.mock import MagicMock, patch
from models.engine import db_storage
from models.state import State
from os import getenv
import MySQLdb



class test_fileStorage(unittest.TestCase):
    """ """

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                    "can't run if storage is file")
    def setUp(self):
        self.storage = db_storage.DBStorage()
        if getenv("HBNB_TYPE_STORAGE") == "db":
            self.db = MySQLdb.connect(getenv("HBNB_MYSQL_HOST"),
                                    getenv("HBNB_MYSQL_USER"),
                                    getenv("HBNB_MYSQL_PWD"),
                                    getenv("HBNB_MYSQL_DB"))
            self.cursor = self.db.cursor()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                    "can't run if storage is file")
    def tearDown(self):
        """at the end of the test this will tear it down"""
        if getenv("HBNB_TYPE_STORAGE") == "db":
            self.db.close()
        
    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                    "can't run if storage is file")
    def test_new_DBStorage(self):
        """Tests for new() method"""
        nb = self.cursor.execute("SELECT COUNT(*) FROM states")
        state = State(name="Oregon")
        state.save()
        nb1 = self.cursor.execute("SELECT COUNT(*) FROM states")
        self.assertEqual(nb1 - nb, 0)

    @patch.object(db_storage.DBStorage, '_DBStorage__session')
    def test_delete_object(self, mock_session):
        mock_obj = MagicMock()
        self.storage.delete(mock_obj)
        mock_session.delete.assert_called_once_with(mock_obj)
    
    @patch.object(db_storage.DBStorage, '_DBStorage__session')
    def test_delete_none(self, mock_session):
        self.storage.delete(None)
        mock_session.delete.assert_not_called()

    @patch.object(db_storage.DBStorage, '_DBStorage__session')
    def test_save(self, mock_session):
        self.storage.save()
        mock_session.commit.assert_called_once()
    
    @patch.object(db_storage.DBStorage, '_DBStorage__session')
    def test_new(self, mock_session):
        mock_obj = MagicMock()
        self.storage.new(mock_obj)
        mock_session.add.assert_called_once_with(mock_obj)

if __name__ == '__main__':
    unittest.main()