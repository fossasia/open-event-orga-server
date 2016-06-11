from flask.ext.restplus import Resource, Namespace, fields

from open_event.models.sponsor import Sponsor as SponsorModel, SponsorType as SponsorTypeModel
from custom_fields import UriField, ImageUriField
from .helpers import get_paginated_list, requires_auth, get_object_in_event
from utils import PAGINATED_MODEL, PaginatedResourceBase, ServiceDAO, \
    PAGE_PARAMS, POST_RESPONSES, PUT_RESPONSES

api = Namespace('sponsors', description='Sponsors', path='/')

SPONSOR = api.model('Sponsor', {
    'id': fields.Integer(required=True),
    'name': fields.String,
    'url': UriField(),
    'logo': ImageUriField(),
    'description': fields.String,
    'sponsor_type_id': fields.Integer,
})

SPONSOR_PAGINATED = api.clone('SponsorPaginated', PAGINATED_MODEL, {
    'results': fields.List(fields.Nested(SPONSOR))
})

SPONSOR_POST = api.clone('SponsorPost', SPONSOR)
del SPONSOR_POST['id']


# Create DAO
class SponsorDAO(ServiceDAO):
    def validate_sponsor_type(self, payload, event_id):
        sponsor_type_id = payload.get('sponsor_type_id', False)
        if sponsor_type_id:
            get_object_in_event(SponsorTypeModel, sponsor_type_id, event_id)

DAO = SponsorDAO(model=SponsorModel)


@api.route('/events/<int:event_id>/sponsors/<int:sponsor_id>')
@api.response(404, 'Sponsor not found')
@api.response(400, 'Sponsor does not belong to event')
class Sponsor(Resource):
    @api.doc('get_sponsor')
    @api.marshal_with(SPONSOR)
    def get(self, event_id, sponsor_id):
        """Fetch a sponsor given its id"""
        return DAO.get(event_id, sponsor_id)

    @requires_auth
    @api.doc('delete_sponsor')
    @api.marshal_with(SPONSOR)
    def delete(self, event_id, sponsor_id):
        """Delete a sponsor given its id"""
        return DAO.delete(event_id, sponsor_id)

    @requires_auth
    @api.doc('update_sponsor', responses=PUT_RESPONSES)
    @api.marshal_with(SPONSOR)
    @api.expect(SPONSOR_POST, validate=True)
    def put(self, event_id, sponsor_id):
        """Update a sponsor given its id"""
        DAO.validate(self.api.payload, SPONSOR_POST)
        DAO.validate_sponsor_type(self.api.payload, event_id)
        return DAO.update(event_id, sponsor_id, self.api.payload)


@api.route('/events/<int:event_id>/sponsors')
class SponsorList(Resource):
    @api.doc('list_sponsors')
    @api.marshal_list_with(SPONSOR)
    def get(self, event_id):
        """List all sponsors"""
        return DAO.list(event_id)

    @requires_auth
    @api.doc('create_sponsor', responses=POST_RESPONSES)
    @api.marshal_with(SPONSOR)
    @api.expect(SPONSOR_POST, validate=True)
    def post(self, event_id):
        """Create a sponsor"""
        DAO.validate(self.api.payload, SPONSOR_POST)
        DAO.validate_sponsor_type(self.api.payload, event_id)
        return DAO.create(event_id, self.api.payload)


@api.route('/events/<int:event_id>/sponsors/page')
class SponsorListPaginated(Resource, PaginatedResourceBase):
    @api.doc('list_sponsors_paginated', params=PAGE_PARAMS)
    @api.marshal_with(SPONSOR_PAGINATED)
    def get(self, event_id):
        """List sponsors in a paginated manner"""
        return get_paginated_list(
            SponsorModel,
            self.api.url_for(self, event_id=event_id),
            args=self.parser.parse_args(),
            event_id=event_id
        )
