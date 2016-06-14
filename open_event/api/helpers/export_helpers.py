import json
import os
import shutil
from flask_restplus import marshal

from ..events import DAO as EventDAO, EVENT
from ..formats import DAO as FormatDAO, FORMAT
from ..languages import DAO as LanguageDAO, LANGUAGE
from ..levels import DAO as LevelDAO, LEVEL
from ..microlocations import DAO as MicrolocationDAO, MICROLOCATION
from ..sessions import DAO as SessionDAO, SESSION
from ..speakers import DAO as SpeakerDAO, SPEAKER
from ..sponsor_types import DAO as SponsorTypeDAO, SPONSOR_TYPE
from ..sponsors import DAO as SponsorDAO, SPONSOR
from ..tracks import DAO as TrackDAO, TRACK


EXPORTS = [
    ('event', EventDAO, EVENT),
    ('formats', FormatDAO, FORMAT),
    ('languages', LanguageDAO, LANGUAGE),
    ('levels', LevelDAO, LEVEL),
    ('microlocations', MicrolocationDAO, MICROLOCATION),
    ('sessions', SessionDAO, SESSION),
    ('speakers', SpeakerDAO, SPEAKER),
    ('sponsor_types', SponsorTypeDAO, SPONSOR_TYPE),
    ('sponsors', SponsorDAO, SPONSOR),
    ('tracks', TrackDAO, TRACK)
]


def export_event_json(event_id):
    """
    Exports the event as a zip on the server and return its path
    """
    # make directory
    dir_path = 'static/exports/event%d' % event_id
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)
    os.mkdir(dir_path)
    # save to directory
    for e in EXPORTS:
        if e[0] == 'event':
            data = marshal(e[1].get(event_id), e[2])
        else:
            data = marshal(e[1].list(event_id), e[2])
        data_str = json.dumps(data, sort_keys=True, indent=4)
        fp = open(dir_path + '/' + e[0] + '.json', 'w')
        fp.write(data_str)
        fp.close()
    # make zip
    shutil.make_archive(dir_path, 'zip', dir_path)
    return os.path.realpath('.') + '/' + dir_path + '.zip'
