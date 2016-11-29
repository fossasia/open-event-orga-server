import unittest
from tests.unittests.utils import OpenEventTestCase
from mock import patch

from tests.unittests.object_mother import ObjectMother
from tests.unittests.setup_database import Setup
from app import current_app as app
from app.models import db
from app.models.version import Version
from app.helpers.data import DataManager, update_version


class TestDataManager(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            db.session.add(ObjectMother.get_event())
            db.session.commit()

    def _delete_object_from_db(self):
        DataManager().remove_microlocation(1)

    @patch.object(db.session, "rollback")
    def test_rollback_called_when_object_doesnt_exist(self, method):
        with app.test_request_context():
            self._delete_object_from_db()
            self.assertTrue(method.called)

    def test_update_version_function(self):
        with app.test_request_context():
            update_version(1, False, "tracks_ver")
            self.assertEqual(Version.query.get(1).id, 1)
            # tracks_ver was 0 at start
            self.assertEqual(Version.query.get(1).tracks_ver, 1)
            update_version(1, False, "tracks_ver")
            self.assertEqual(Version.query.get(1).tracks_ver, 2)
            self.assertEqual(Version.query.get(2), None)

    def test_no_increasing_version_after_update_version_called(self):
        with app.test_request_context():
            # as event has been created so version is already created
            self.assertEqual(len(Version.query.all()), 1)
            update_version(1, False, "tracks_ver")
            self.assertEqual(len(Version.query.all()), 1)


if __name__ == '__main__':
    unittest.main()
