import unittest
from datetime import timedelta, datetime, timezone

from app import current_app as app, db
from app.api.helpers import ticketing
from app.api.helpers.order import set_expiry_for_order, delete_related_attendees_for_order
from app.factories.attendee import AttendeeFactory
from app.factories.order import OrderFactory
from app.models.order import Order
from tests.unittests.setup_database import Setup
from tests.unittests.utils import OpenEventTestCase


class TestOrderUtilities(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_should_expire_outdated_order(self):
        with app.test_request_context():
            obj = OrderFactory()
            obj.created_at = datetime.now(timezone.utc) - timedelta(
                minutes=ticketing.TicketingManager.get_order_expiry() + 10)
            set_expiry_for_order(obj)
            self.assertEqual(obj.status, 'expired')

    def test_should_not_expire_valid_orders(self):
        with app.test_request_context():
            obj = OrderFactory()
            set_expiry_for_order(obj)
            self.assertEqual(obj.status, 'pending')

    def test_should_delete_related_attendees(self):
        with app.test_request_context():
            attendee = AttendeeFactory()
            db.session.add(attendee)
            db.session.commit()

            obj = OrderFactory()
            obj.ticket_holders = [attendee, ]
            db.session.add(obj)
            db.session.commit()

            delete_related_attendees_for_order(obj)
            order = db.session.query(Order).filter(Order.id == obj.id).first()
            self.assertEqual(len(order.ticket_holders), 0)


if __name__ == '__main__':
    unittest.main()
