import unittest
import json
import logging
import shutil
import time
import os
from StringIO import StringIO

from tests.setup_database import Setup
from tests.utils import OpenEventTestCase
from tests.api.utils import create_event, get_path, create_services,\
    create_session, save_to_db, Speaker
from tests.auth_helper import register
from open_event import current_app as app


class TestEventExport(OpenEventTestCase):
    """
    Test export of event
    """
    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            create_event()
            create_services(1)

    def test_export_success(self):
        path = get_path(1, 'export', 'json')
        resp = self.app.get(path)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('event1.zip', resp.headers['Content-Disposition'])
        size = len(resp.data)
        with app.test_request_context():
            create_services(1, '2')
            create_services(1, '3')
        # check if size increased
        resp = self.app.get(path)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) > size)

    def test_export_no_event(self):
        path = get_path(2, 'export', 'json')
        resp = self.app.get(path)
        self.assertEqual(resp.status_code, 404)


class TestEventImport(OpenEventTestCase):
    """
    Test import of event
    """
    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            create_event(creator_email='test@example.com')
            create_services(1, '1')
            create_services(1, '2')
            create_services(1, '3')

    def _upload(self, data, url, filename='anything'):
        return self.app.post(
            url,
            data={'file': (StringIO(data), filename)}
        )

    def _test_import_success(self):
        # first export
        path = get_path(1, 'export', 'json')
        resp = self.app.get(path)
        file = resp.data
        self.assertEqual(resp.status_code, 200)
        # import
        upload_path = get_path('import', 'json')
        resp = self._upload(file, upload_path, 'event.zip')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('task_url', resp.data)
        task_url = json.loads(resp.data)['task_url']
        # wait for done
        while True:
            resp = self.app.get(task_url)
            if 'SUCCESS' in resp.data:
                self.assertIn('result', resp.data)
                dic = json.loads(resp.data)['result']
                break
            logging.info(resp.data)
            time.sleep(2)
        # check internals
        self.assertEqual(dic['id'], 2)
        self.assertEqual(dic['name'], 'TestEvent')
        self.assertIn('fb.com', json.dumps(dic['social_links']), dic)
        # get to check final
        resp = self.app.get(get_path(2))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('TestEvent', resp.data)
        # No errors generally means everything went fine
        # The method will crash and return 500 in case of any problem

    def _test_import_error(self, checks=[]):
        # first export
        path = get_path(1, 'export', 'json')
        resp = self.app.get(path)
        file = resp.data
        self.assertEqual(resp.status_code, 200)
        # import
        upload_path = get_path('import', 'json')
        resp = self._upload(file, upload_path, 'event.zip')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('task_url', resp.data)
        task_url = json.loads(resp.data)['task_url']
        # wait for done
        while True:
            resp = self.app.get(task_url)
            if resp.status_code != 200:
                break
            logging.info(resp.data)
            time.sleep(2)
        # checks
        for i in checks:
            self.assertIn(i, resp.data, resp.data)

    def test_import_simple(self):
        self._test_import_success()

    def test_import_extended(self):
        with app.test_request_context():
            create_session(
                1, '4', track=1, session_type=1,
                microlocation=1, speakers=[2, 3])
            create_session(
                1, '5', track=2, speakers=[1]
            )
        self._test_import_success()

    def test_import_validation_error(self):
        """
        tests if error is returned correctly.
        Needed after task was run through celery
        """
        with app.test_request_context():
            speaker = Speaker(
                name='SP',
                email='invalid_email',
                organisation='org',
                country='japan',
                event_id=1)
            save_to_db(speaker, 'speaker invalid saved')
        self._test_import_error(
            checks=['Invalid', 'email', '400']
        )


class TestImportOTS(OpenEventTestCase):
    """
    Tests import of OTS sample
    """
    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')

    def _upload(self, data, url, filename='anything'):
        return self.app.post(
            url,
            data={'file': (StringIO(data), filename)}
        )

    def _test_import_ots(self):
        dir_path = 'samples/ots16'
        shutil.make_archive(dir_path, 'zip', dir_path)
        file = open(dir_path + '.zip', 'r').read()
        os.remove(dir_path + '.zip')
        upload_path = get_path('import', 'json')
        resp = self._upload(file, upload_path, 'event.zip')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Open Tech Summit', resp.data)


if __name__ == '__main__':
    unittest.main()
