import unittest

from app import current_app as app
from app.factories.attendee import AttendeeFactory
from app.models.ticket_holder import TicketHolder
from tests.unittests.utils import OpenEventTestCase
from app.factories.event import EventFactoryBasic
from app.api.helpers.db import save_to_db, safe_query, get_or_create, get_count
from flask_rest_jsonapi.exceptions import ObjectNotFound
from app.models import db
from app.models.event import Event
from tests.unittests.setup_database import Setup


class TestDBHelperValidation(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_save_to_db(self):
        with app.test_request_context():
            obj = EventFactoryBasic()
            save_to_db(obj)
            event = db.session.query(Event).filter(Event.id == obj.id).first()
            self.assertEqual(obj.name, event.name)

    def test_safe_query(self):
        with app.test_request_context():
            event = EventFactoryBasic()
            db.session.add(event)
            db.session.commit()
            obj = safe_query(db, Event, 'id', event.id, 'event_id')
            self.assertEqual(obj.name, event.name)

    def test_safe_query_exception(self):
        with app.test_request_context():
            self.assertRaises(ObjectNotFound, lambda: safe_query(db, Event, 'id', 1, 'event_id'))

    def test_get_or_create(self):
        with app.test_request_context():
            event = EventFactoryBasic()
            save_to_db(event)
            obj, is_created = get_or_create(Event, name=event.name)
            self.assertEqual(event.id, obj.id)
            self.assertFalse(is_created)

            obj, is_created = get_or_create(Event, name="new event", starts_at=event.starts_at, ends_at=event.ends_at)
            self.assertNotEqual(event.id, obj.id)
            self.assertTrue(is_created)

    def test_get_count(self):
        with app.test_request_context():
            attendee = AttendeeFactory()
            save_to_db(attendee)
            self.assertEqual(get_count(TicketHolder.query), 1)

if __name__ == '__main__':
    unittest.main()
