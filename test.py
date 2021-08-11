from app import app
from unittest import TestCase
from converting import *

def setUp(self):

    self.client = app.test_client()
    app.configt['TESTING'] = True

def test_users_index(self):
    """tests index.html for title"""
    response = self.get("/users/index")
    assert response.data == b'Users'

def test_users_new(self):
    """tests new.html for title"""
    response = self.get("/users/new")
    assert response.data == b'Create new user'

def test_users_edit(self):
    """tests edit.html for title"""
    response = self.get("/users/edit")
    assert response.data == b'Edit'

def test_users_show(self):
    """tests show.html for status code"""
    response = self.get("/users/show")
    assert response.status_code == 200

