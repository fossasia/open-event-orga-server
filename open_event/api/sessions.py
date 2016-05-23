from flask.ext.restplus import Resource, Namespace, fields

from open_event.models.session import Session as SessionModel
from open_event.models.event import Event as EventModel
from .helpers import get_object_list, get_object_or_404

api = Namespace('sessions', description='Sessions', path='/')

track = api.model('Track', {
    'id': fields.Integer(required=True),
    'name': fields.String,
})

speaker = api.model('Speaker', {
    'id': fields.Integer(required=True),
    'name': fields.String,
})

level = api.model('Level', {
    'id': fields.Integer(required=True),
    'label_en': fields.String,
})

language = api.model('Language', {
    'id': fields.Integer(required=True),
    'label_en': fields.String,
    'label_de': fields.String,
})

microlocation = api.model('Microlocation', {
    'id': fields.Integer(required=True),
    'name': fields.String,
})

session = api.model('Session', {
    'id': fields.Integer(required=True),
    'title': fields.String,
    'subtitle': fields.String,
    'abstract': fields.String,
    'description': fields.String,
    'start_time': fields.DateTime,
    'end_time': fields.DateTime,
    'track': fields.Nested(track),
    'speakers': fields.List(fields.Nested(speaker)),
    'level': fields.Nested(level),
    'language': fields.Nested(language),
    'microlocation': fields.Nested(microlocation),
})


@api.route('/events/<int:event_id>/sessions/<int:id>')
@api.param('id')
@api.response(404, 'Session not found')
class Session(Resource):
    @api.doc('get_session')
    @api.marshal_with(session)
    def get(self, event_id, id):
        """Fetch a session given its id"""
        # Check if an event with `event_id` exists
        get_object_or_404(EventModel, event_id)

        return get_object_or_404(SessionModel, id)


@api.route('/events/<int:event_id>/sessions')
@api.param('event_id')
class SessionList(Resource):
    @api.doc('list_sessions')
    @api.marshal_list_with(session)
    def get(self, event_id):
        """List all sessions"""
        # Check if an event with `event_id` exists
        get_object_or_404(EventModel, event_id)

        return get_object_list(SessionModel, event_id=event_id)
