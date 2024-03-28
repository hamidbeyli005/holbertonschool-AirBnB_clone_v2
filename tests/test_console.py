#!/usr/bin/python3

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from console import HBNBCommand
import unittest
from unittest.mock import patch
from io import StringIO



class TestConsole(unittest.TestCase):

    def setUp(self):
        self.hbtn = HBNBCommand()
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_without_className(self, mock_stdout):
        self.hbtn.onecmd("create")
        self.assertEqual(mock_stdout.getvalue(),"** class name missing **\n")    
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_invalid_class(self, mock_stdout):
        self.hbtn.onecmd("create InvaliClass")
        self.assertEqual(mock_stdout.getvalue(),"** class doesn't exist **\n")
        
    @patch('sys.stdout',new_callable=StringIO)
    def test_create_valid_class(self, mock_stdout):
        self.hbtn.onecmd("create State")
        self.assertTrue(mock_stdout.getvalue() != "")


