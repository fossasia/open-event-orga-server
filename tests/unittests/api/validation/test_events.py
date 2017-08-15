import unittest
from datetime import datetime
from pytz import timezone

from app import current_app as app
from tests.unittests.utils import OpenEventTestCase
from app.api.helpers.exceptions import UnprocessableEntity
from app.api.schema.events import EventSchema
from app.factories.event import EventFactoryBasic
from app.models import db
from tests.unittests.setup_database import Setup


class TestEventValidation(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_date_pass(self):
        """
        Events Validate Date - Tests if the function runs without an exception
        :return:
        """
        schema = EventSchema()
        original_data = {
            'data': {}
        }
        data = {
            'starts_at': datetime(2003, 8, 4, 12, 30, 45).replace(tzinfo=timezone('UTC')),
            'ends_at': datetime(2003, 9, 4, 12, 30, 45).replace(tzinfo=timezone('UTC'))
        }
        EventSchema.validate_date(schema, data, original_data)

    def test_date_start_gt_end(self):
        """
        Events Validate Date - Tests if exception is raised when ends_at is before starts_at
        :return:
        """
        schema = EventSchema()
        original_data = {
            'data': {}
        }
        data = {
            'starts_at': datetime(2003, 9, 4, 12, 30, 45).replace(tzinfo=timezone('UTC')),
            'ends_at': datetime(2003, 8, 4, 12, 30, 45).replace(tzinfo=timezone('UTC'))
        }
        with self.assertRaises(UnprocessableEntity):
            EventSchema.validate_date(schema, data, original_data)

    def test_date_db_populate(self):
        """
        Events Validate Date - Tests if validation works on values stored in db and not given in 'data'
        :return:
        """
        with app.test_request_context():
            schema = EventSchema()
            obj = EventFactoryBasic()
            db.session.add(obj)
            db.session.commit()

            original_data = {
                'data': {
                    'id': 1
                }
            }
            data = {}
            EventSchema.validate_date(schema, data, original_data)


if __name__ == '__main__':
    unittest.main()
