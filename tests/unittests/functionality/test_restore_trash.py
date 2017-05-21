import unittest
from datetime import datetime

from app import current_app as app
from app.helpers.data import restore_event, restore_session, restore_user
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

    def test_restore_event_from_trash(self):
        with app.test_request_context():
            event = Event(name="event1",
                          starts_at=datetime(2003, 8, 4, 12, 30, 45),
                          ends_at=datetime(2003, 9, 4, 12, 30, 45),
                          deleted_at=datetime.now())

            save_to_db(event, "Event saved")
            restore_event(1)
            self.assertEqual(event.deleted_at, None)

    def test_restore_user_from_trash(self):
        with app.test_request_context():
            user = User(password="test",
                        email="email@gmail.com",
                        deleted_at=datetime.now())

            save_to_db(user, "User saved")
            restore_user(1)
            self.assertEqual(user.deleted_at, None)

    def test_restore_session_from_trash(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            session = Session(title='Session 1',
                              long_abstract='dsad',
                              starts_at=datetime(2003, 8, 4, 12, 30, 45),
                              ends_at=datetime(2003, 8, 4, 12, 30, 45),
                              event_id=1,
                              state='pending',
                              deleted_at=datetime.now())

            save_to_db(event, "Event saved")
            save_to_db(session, "Session saved")
            restore_session(1)
            self.assertEqual(session.deleted_at, None)


if __name__ == '__main__':
    unittest.main()
