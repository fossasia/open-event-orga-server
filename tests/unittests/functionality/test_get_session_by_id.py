import unittest
from tests.unittests.utils import OpenEventTestCase
from tests.unittests.object_mother import ObjectMother
from app import current_app as app
from app.helpers.data import save_to_db


class TestGetSessionById(OpenEventTestCase):
    def test_get_session_by_id(self):
        session = ObjectMother.get_session()
        with app.test_request_context():
            save_to_db(session, "Session saved")
            response = self.app.get('/api/v1/event/sessions/1')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
