import unittest
from datetime import datetime

from flask import url_for

from app import current_app as app
from app.helpers.data import DataManager, trash_user, trash_session
from app.helpers.data import save_to_db
from app.models.event import Event
from app.models.session import Session
from app.models.user import User
from tests.unittests.object_mother import ObjectMother
from tests.unittests.setup_database import Setup
from tests.unittests.utils import OpenEventTestCase


class TestAdminTrash(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_add_event_to_trash(self):
        with app.test_request_context():
            event = Event(name="event1",
                          starts_at=datetime(2003, 8, 4, 12, 30, 45),
                          ends_at=datetime(2003, 9, 4, 12, 30, 45),
                          deleted_at=None)

            save_to_db(event, "Event saved")
            DataManager.trash_event(1)
            url = url_for('events.index_view')
            rv = self.app.get(url)
            self.assertFalse('event1' in rv.data)
            self.assertTrue(event.deleted_at is not None)

    def test_add_user_to_trash(self):
        with app.test_request_context():
            user = User(password="test",
                        email="email@gmail.com",
                        deleted_at=None)

            save_to_db(user, "User saved")
            trash_user(1)
            self.assertTrue(user.deleted_at is not None)

    def test_add_session_to_trash(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            session = Session(title='Session 1',
                              long_abstract='dsad',
                              starts_at=datetime(2003, 8, 4, 12, 30, 45),
                              ends_at=datetime(2003, 8, 4, 12, 30, 45),
                              event_id=1,
                              state='pending',
                              deleted_at=None)

            save_to_db(event, "Event saved")
            save_to_db(session, "Session saved")
            trash_session(1)
            url = url_for('event_sessions.index_view', event_id=1)
            rv = self.app.get(url)
            self.assertFalse('Session 1' in rv.data)
            self.assertTrue(session.deleted_at is not None)


if __name__ == '__main__':
    unittest.main()
