from flask import Blueprint, render_template
from flask.ext.restplus import Api
from flask_login import current_user

from .events import api as event_api
from .sessions import api as session_api
from .tracks import api as track_api
from .speakers import api as speaker_api
from .sponsors import api as sponsor_api
from .microlocations import api as microlocation_api
from .levels import api as level_api
from .formats import api as format_api
from .languages import api as language_api
from .login import api as login_api

api_v2 = Blueprint('api', __name__, url_prefix='/api/v2')

api = Api(api_v2, version='2.0', title='Organizer Server APIs',
          description='Open Event Organizer APIs')

api.add_namespace(event_api)
api.add_namespace(session_api)
api.add_namespace(track_api)
api.add_namespace(speaker_api)
api.add_namespace(sponsor_api)
api.add_namespace(microlocation_api)
api.add_namespace(level_api)
api.add_namespace(format_api)
api.add_namespace(language_api)
api.add_namespace(login_api)


@api.documentation
def custom_ui():
    return render_template(
        'swagger/swagger-ui.html',
        title=api.title,
        specs_url=api.specs_url,
        user=current_user)
