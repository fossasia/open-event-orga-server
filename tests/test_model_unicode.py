# -*- coding: utf-8 -*-
from datetime import datetime
import unittest

from tests.setup_database import Setup
from tests.utils import OpenEventTestCase

from open_event import current_app as app
from open_event.helpers.data import save_to_db
from open_event.models.event import Event
from open_event.models.session import Session, Level, Format, Language
from open_event.models.speaker import Speaker
from open_event.models.sponsor import Sponsor
from open_event.models.microlocation import Microlocation

UNICODE_STRING = u'☺'


class TestModelUnicode(OpenEventTestCase):
    """
    Tests for unicode handling in models
    """
    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            event = Event(name=UNICODE_STRING,
                          start_time=datetime(2013, 8, 4, 12, 30, 45),
                          end_time=datetime(2016, 9, 4, 12, 30, 45))
            event.owner = 1

            microlocation = Microlocation(name=UNICODE_STRING)
            level = Level(name=UNICODE_STRING, event_id=1)
            session_format = Format(name=UNICODE_STRING, label_en='label',
                                    event_id=1)
            language = Language(name=UNICODE_STRING, event_id=1)
            session = Session(title=UNICODE_STRING, description='descp',
                              start_time=datetime(2014, 8, 4, 12, 30, 45),
                              end_time=datetime(2015, 9, 4, 12, 30, 45))
            speaker = Speaker(name=UNICODE_STRING, email='email@eg.com',
                              organisation='org', country='japan')
            sponsor = Sponsor(name=UNICODE_STRING)

            save_to_db(event, "Event saved")
            save_to_db(microlocation, 'Microlocation saved')
            save_to_db(level, 'Level saved')
            save_to_db(session_format, 'Format saved')
            save_to_db(language, 'Language saved')
            save_to_db(session, 'Session saved')
            save_to_db(speaker, 'Speaker saved')
            save_to_db(sponsor, 'Sponsor saved')

    def test_event_name(self):
        """Unicode handling for Event model"""
        with app.test_request_context():
            try:
                str(Event.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for event')

    def test_microlocation_name(self):
        """Unicode handling for Microlocation model"""
        with app.test_request_context():
            try:
                str(Microlocation.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for microlocation')

    def test_level_name(self):
        """Unicode handling for Level model"""
        with app.test_request_context():
            try:
                str(Level.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for level')

    def test_format_name(self):
        """Unicode handling for Format model"""
        with app.test_request_context():
            try:
                str(Format.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for format')

    def test_language_name(self):
        """Unicode handling for Language model"""
        with app.test_request_context():
            try:
                str(Language.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for language')

    def test_session_title(self):
        """Unicode handling for Session model"""
        with app.test_request_context():
            try:
                str(Session.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for session')

    def test_sponsor_name(self):
        """Unicode handling for Sponsor model"""
        with app.test_request_context():
            try:
                str(Sponsor.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for sponsor')

    def test_speaker_name(self):
        """Unicode handling for Speaker model"""
        with app.test_request_context():
            try:
                str(Speaker.query.get(1))
            except UnicodeEncodeError:
                self.fail('UnicodeEncodeError for speaker')


if __name__ == '__main__':
    unittest.main()
