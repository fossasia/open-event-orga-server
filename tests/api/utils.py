from datetime import datetime

from open_event.helpers.data import save_to_db
from open_event.models.event import Event
from open_event.models.session import Session, Level, Format, Language
from open_event.models.speaker import Speaker
from open_event.models.sponsor import Sponsor
from open_event.models.microlocation import Microlocation
from open_event.models.track import Track


def create_event(name='TestEvent'):
    """Creates Event and returns its `id`.
    :param name Name of Event
    """
    event = Event(name=name,
                  start_time=datetime(2013, 8, 4, 12, 30, 45),
                  end_time=datetime(2016, 9, 4, 12, 30, 45))
    event.owner = 1

    save_to_db(event, 'Event saved')
    return event.id


def create_services(event_id, serial_no=''):
    """Creates services and associates them with `event_id`. Service names
    have an optional `serial_no` that can be used to make them unique.
    """
    test_micro = 'TestMicrolocation{}_{}'.format(serial_no, event_id)
    test_track = 'TestTrack{}_{}'.format(serial_no, event_id)
    test_level = 'TestLevel{}_{}'.format(serial_no, event_id)
    test_format = 'TestFormat{}_{}'.format(serial_no, event_id)
    test_lang = 'TestLanguage{}_{}'.format(serial_no, event_id)
    test_session = 'TestSession{}_{}'.format(serial_no, event_id)
    test_speaker = 'TestSpeaker{}_{}'.format(serial_no, event_id)
    test_sponsor = 'TestSponsor{}_{}'.format(serial_no, event_id)

    microlocation = Microlocation(name=test_micro, event_id=event_id)
    track = Track(
        name=test_track,
        description='descp',
        event_id=event_id,
        color='red'
    )
    level = Level(name=test_level, event_id=event_id)
    format_ = Format(name=test_format, label_en='label', event_id=event_id)
    language = Language(name=test_lang, event_id=event_id)
    session = Session(title=test_session,
                      description='descp',
                      start_time=datetime(2014, 8, 4, 12, 30, 45),
                      end_time=datetime(2015, 9, 4, 12, 30, 45),
                      event_id=event_id)
    speaker = Speaker(name=test_speaker,
                      email='email@eg.com',
                      organisation='org',
                      country='japan',
                      event_id=event_id)
    sponsor = Sponsor(name=test_sponsor, event_id=event_id)

    save_to_db(microlocation, 'Microlocation saved')
    save_to_db(track, 'Track saved')
    save_to_db(level, 'Level saved')
    save_to_db(format_, 'Format saved')
    save_to_db(language, 'Language saved')
    save_to_db(session, 'Session saved')
    save_to_db(speaker, 'Speaker saved')
    save_to_db(sponsor, 'Sponsor saved')


def get_path(*args):
    """Returns API base path with passed arguments appended as path
    parameters.

    '/api/v2/events' + '/arg1/arg2/arg3'

    e.g. create_url(2, 'tracks', 7) -> '/api/v2/events/2/tracks/7'
    """
    url = '/api/v2/events'
    if args:
        url += '/' + '/'.join(map(str, args))
    return url
