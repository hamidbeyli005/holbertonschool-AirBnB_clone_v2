#!/usr/bin/python3
""" """
import unittest
from unittest.mock import MagicMock, patch
from models.engine import db_storage


class test_fileStorage(unittest.TestCase):
    """ """

    def setUp(self):
        self.storage = db_storage.DBStorage()

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