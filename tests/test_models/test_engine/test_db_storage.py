import unittest
from unittest.mock import MagicMock, patch
from models.engine import db_storage
from models.state import State

class TestDBStorage(unittest.TestCase):
    def setUp(self):
        self.storage = db_storage.DBStorage()

    @patch.object(db_storage.DBStorage, '_DBStorage__session')
    def test_all_with_class(self, mock_session):
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        self.storage.all(State)
        mock_session.query.assert_called_once_with(State)
        mock_query.all.assert_called_once()

    @patch.object(db_storage.DBStorage, '_DBStorage__session')
    def test_all_without_class(self, mock_session):
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        self.storage.all()
        assert mock_session.query.call_count == len(db_storage.classes)
        mock_query.all.assert_called()

if __name__ == '__main__':
    unittest.main()