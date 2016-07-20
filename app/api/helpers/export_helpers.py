import json
import os
import shutil
import requests
from flask_restplus import marshal

from ..events import DAO as EventDAO, EVENT, \
    LinkDAO as SocialLinkDAO, SOCIAL_LINK
from ..microlocations import DAO as MicrolocationDAO, MICROLOCATION
from ..sessions import DAO as SessionDAO, SESSION, \
    TypeDAO as SessionTypeDAO, SESSION_TYPE
from ..speakers import DAO as SpeakerDAO, SPEAKER
from ..sponsors import DAO as SponsorDAO, SPONSOR
from ..tracks import DAO as TrackDAO, TRACK
from .non_apis import CustomFormDAO, CUSTOM_FORM
from import_helpers import is_downloadable, get_filename_from_cd


EXPORTS = [
    ('event', EventDAO, EVENT),
    ('microlocations', MicrolocationDAO, MICROLOCATION),
    ('sessions', SessionDAO, SESSION),
    ('speakers', SpeakerDAO, SPEAKER),
    ('sponsors', SponsorDAO, SPONSOR),
    ('tracks', TrackDAO, TRACK),
    ('session_types', SessionTypeDAO, SESSION_TYPE),
    ('social_links', SocialLinkDAO, SOCIAL_LINK),
    ('custom_forms', CustomFormDAO, CUSTOM_FORM)
]

# keep sync with storage.UPLOAD_PATHS
DOWNLOAD_FIEDLS = {
    'sessions': {
        'video': ['video', '/videos/session_%d'],
        'audio': ['audio', '/audios/session_%d'],
        'slides': ['document', '/slides/session_%d']
    },
    'speakers': {
        'photo': ['image', '/images/speakers/photo_%d']
    },
    'event': {
        'logo': ['image', '/images/logo'],
        'background_url': ['image', '/images/background']
    },
    'sponsors': {
        'logo': ['image', '/images/sponsors/logo_%d']
    },
    'tracks': {
        'track_image_url': ['image', '/images/tracks/image_%d']
    }
}


def _download_media(data, srv, dir_path, settings):
    """
    Downloads the media and saves it
    """
    if srv not in DOWNLOAD_FIEDLS:
        return
    for i in DOWNLOAD_FIEDLS[srv]:
        if not data[i]:
            continue
        if not settings[DOWNLOAD_FIEDLS[srv][i][0]]:
            continue
        path = DOWNLOAD_FIEDLS[srv][i][1]
        if srv != 'event':
            path = path % (data['id'])
        if data[i].find('.') > -1:  # add extension
            ext = data[i].rsplit('.', 1)[1]
            if ext.find('/') == -1:
                path += '.' + ext
        full_path = dir_path + path
        # make dir
        cdir = full_path.rsplit('/', 1)[0]
        if not os.path.isdir(cdir):
            os.makedirs(cdir)
        # download and set
        url = data[i]
        if not is_downloadable(url):
            continue
        try:
            r = requests.get(url, allow_redirects=True)
            ext = get_filename_from_cd(r.headers.get('content-disposition'))[1]
            full_path += ext
            path += ext
            open(full_path, 'wb').write(r.content)
            data[i] = path
        except Exception:
            pass


def export_event_json(event_id, settings):
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
            _download_media(data, 'event', dir_path, settings)
        else:
            data = marshal(e[1].list(event_id), e[2])
            for _ in data:
                _download_media(_, e[0], dir_path, settings)
        data_str = json.dumps(data, sort_keys=True, indent=4)
        fp = open(dir_path + '/' + e[0] + '.json', 'w')
        fp.write(data_str)
        fp.close()
    # make zip
    shutil.make_archive(dir_path, 'zip', dir_path)
    return os.path.realpath('.') + '/' + dir_path + '.zip'
