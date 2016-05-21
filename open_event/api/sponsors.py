from flask.ext.restplus import Resource, Namespace, fields

from open_event.models.sponsor import Sponsor as SponsorModel
from open_event.models.event import Event as EventModel
from .helpers import get_object_list, get_object_or_404

api = Namespace('sponsors', description='sponsors', path='/')

sponsor = api.model('sponsor', {
    'id': fields.Integer(required=True),
    'name': fields.String,
    'url': fields.String,
    'logo': fields.String,
})


@api.route('/events/<int:event_id>/sponsors/<int:id>')
@api.param('id')
@api.response(404, 'sponsor not found')
class Sponsor(Resource):
    @api.doc('get_sponsor')
    @api.marshal_with(sponsor)
    def get(self, event_id, id):
        """Fetch a sponsor given its id"""
        # Check if an event with `event_id` exists
        get_object_or_404(EventModel, event_id)

        return get_object_or_404(SponsorModel, id)


@api.route('/events/<int:event_id>/sponsors')
@api.param('event_id')
class SponsorList(Resource):
    @api.doc('list_sponsors')
    @api.marshal_list_with(sponsor)
    def get(self, event_id):
        """List all sessions"""
        # Check if an event with `event_id` exists
        get_object_or_404(EventModel, event_id)

        return get_object_list(SponsorModel, event_id=event_id)
