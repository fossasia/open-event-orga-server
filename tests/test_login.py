"""Copyright 2015 Rafal Kowalski"""
import unittest
from auth_helper import register
import unittest
from flask import url_for
from tests.set_up import Setup
from open_event import current_app as app
from open_event.helpers.data import save_to_db
from tests.object_mother import ObjectMother
from tests.auth_helper import register, logout, login


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, 'test', 'email@gmail.com', 'test')

    def tearDown(self):
        Setup.drop_db()

    def test_registration(self):
        rv = register(self.app,'test', 'email@gmail.com', 'test')
        self.assertTrue('The FOSSASIA Open Event' in rv.data)

    def test_logout(self):
        register(self.app,'test', 'email@gmail.com', 'test')
        rv = logout(self.app)
        self.assertTrue("Don't have an account?" in rv.data)

    def test_login(self):
        register(self.app,'test', 'email@gmail.com', 'test')
        logout(self.app)
        rv = login(self.app, 'test', 'test')
        self.assertTrue("The FOSSASIA Open Event" in rv.data)