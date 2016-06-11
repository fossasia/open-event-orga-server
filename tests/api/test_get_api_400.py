import unittest

from tests.setup_database import Setup
from tests.utils import OpenEventTestCase
from tests.api.utils import get_path, create_event, create_services

from open_event import current_app as app


class TestGetApiUnrelatedServices(OpenEventTestCase):
    """Test 400 response code for services that don't belong the said event.

    e.g. A Track with id 3 exists and and Event with id 2 exists, but the
    Track doesn't belong to the Event. The following path should give a 400
    response code: '/api/v2/events/2/tracks/3'

    Services include Session, Track, Language, etc. (everything except Event)
    """

    def setUp(self):
        """Create Event (it will have id = `event_id`). Create services and
        associate them with event id = `event_id` + 1.
        """
        self.app = Setup.create_app()
        with app.test_request_context():
            # `event_id` is going to be 1
            event_id = create_event()
            # Associate services to event_id=2
            # No need to create the event though
            create_services(event_id+1)

    def _test_path(self, path):
        """Test response for 400 status code. Also test if response body
        contains 'does not belong to event' string.
        """
        with app.test_request_context():
            response = self.app.get(path)
            self.assertEqual(response.status_code, 400)
            self.assertIn('does not belong to event', response.data)


    def test_microlocation_api(self):
        path = get_path(1, 'microlocations', 1)
        self._test_path(path)

    def test_track_api(self):
        path = get_path(1, 'tracks', 1)
        self._test_path(path)

    def test_level_api(self):
        path = get_path(1, 'levels', 1)
        self._test_path(path)

    def test_format_api(self):
        path = get_path(1, 'formats', 1)
        self._test_path(path)

    def test_language_api(self):
        path = get_path(1, 'languages', 1)
        self._test_path(path)

    def test_session_api(self):
        path = get_path(1, 'sessions', 1)
        self._test_path(path)

    def test_speaker_api(self):
        path = get_path(1, 'speakers', 1)
        self._test_path(path)

    def test_sponsor_api(self):
        path = get_path(1, 'sponsors', 1)
        self._test_path(path)

    def test_sponsor_type_api(self):
        path = get_path(1, 'sponsor_types', 1)
        self._test_path(path)


if __name__ == '__main__':
    unittest.main()
