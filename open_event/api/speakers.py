from flask.ext.restplus import Resource, Namespace, fields

from open_event.models.speaker import Speaker as SpeakerModel
from open_event.models.event import Event as EventModel
from .helpers import get_object_list, get_object_or_404, get_object_in_event

api = Namespace('speakers', description='Speakers', path='/')

SESSION = api.model('Session', {
    'id': fields.Integer,
    'title': fields.String,
})

SPEAKER = api.model('Speaker', {
    'id': fields.Integer(required=True),
    'name': fields.String,
    'photo': fields.String,
    'biography': fields.String,
    'email': fields.String,
    'web': fields.String,
    'twitter': fields.String,
    'facebook': fields.String,
    'github': fields.String,
    'linkedin': fields.String,
    'organisation': fields.String,
    'position': fields.String,
    'country': fields.String,
    'sessions': fields.List(fields.Nested(SESSION)),
})


@api.route('/events/<int:event_id>/speakers/<int:speaker_id>')
@api.response(404, 'Speaker not found')
@api.response(400, 'Object does not belong to event')
class Speaker(Resource):
    @api.doc('get_speaker')
    @api.marshal_with(SPEAKER)
    def get(self, event_id, speaker_id):
        """Fetch a speaker given its id"""
        return get_object_in_event(SpeakerModel, speaker_id, event_id)


@api.route('/events/<int:event_id>/speakers')
@api.param('event_id')
class SpeakerList(Resource):
    @api.doc('list_speakers')
    @api.marshal_list_with(SPEAKER)
    def get(self, event_id):
        """List all speakers"""
        # Check if an event with `event_id` exists
        get_object_or_404(EventModel, event_id)

        return get_object_list(SpeakerModel, event_id=event_id)
