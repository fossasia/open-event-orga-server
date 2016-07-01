from flask.ext.restplus import Resource, Namespace, reqparse
from flask import g

from open_event.models.event import Event as EventModel
from open_event.models.social_link import SocialLink as SocialLinkModel
from open_event.models.users_events_roles import UsersEventsRoles
from open_event.models.role import Role
from open_event.models.user import ORGANIZER
from open_event.helpers.data import save_to_db, update_version, record_activity, \
    get_or_create

from .helpers.helpers import get_paginated_list, requires_auth, parse_args, handle_extra_payload
from .helpers.utils import PAGINATED_MODEL, PaginatedResourceBase, \
    PAGE_PARAMS, POST_RESPONSES, PUT_RESPONSES, BaseDAO, ServiceDAO
from .helpers import custom_fields as fields
from helpers.special_fields import EventTypeField, EventTopicField, \
    EventPrivacyField

api = Namespace('events', description='Events')

EVENT_CREATOR = api.model('EventCreator', {
    'id': fields.Integer(),
    'email': fields.Email()
})

EVENT_SOCIAL = api.model('EventSocial', {
    'id': fields.Integer(),
    'name': fields.String(),
    'link': fields.String()
})

EVENT = api.model('Event', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'email': fields.Email(),
    'color': fields.Color(),
    'logo': fields.ImageUri(),
    'start_time': fields.DateTime(required=True),
    'end_time': fields.DateTime(required=True),
    'timezone': fields.String(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'event_url': fields.Uri(),
    'background_url': fields.ImageUri(),
    'description': fields.String(),
    'location_name': fields.String(),
    'organizer_name': fields.String(),
    'organizer_description': fields.String(),
    'state': fields.String(),
    'closing_datetime': fields.DateTime(),
    'type': EventTypeField(),
    'topic': EventTopicField(),
    'sub_topic': fields.String(),
    'privacy': EventPrivacyField(),
    'ticket_url': fields.Uri(),
    'creator': fields.Nested(EVENT_CREATOR, allow_null=True),
    'schedule_published_on': fields.DateTime(),
    'code_of_conduct': fields.String(),
    'social_links': fields.List(fields.Nested(EVENT_SOCIAL), attribute='social_link')
})

EVENT_PAGINATED = api.clone('EventPaginated', PAGINATED_MODEL, {
    'results': fields.List(fields.Nested(EVENT))
})

EVENT_POST = api.clone('EventPost', EVENT)
SOCIAL_LINK_POST = api.clone('SocialLinkPost', EVENT_SOCIAL)

del EVENT_POST['id']
del EVENT_POST['creator']
# del EVENT_POST['social_links']

del SOCIAL_LINK_POST['id']


# ###################
# Data Access Objects
# ###################


class SocialLinkDAO(ServiceDAO):
    """
    Social Link DAO
    """
    pass


class EventDAO(BaseDAO):
    """
    Event DAO
    """

    def fix_payload(self, data):
        """
        Fixes the payload data.
        Here converts string time from datetime obj
        """
        data['start_time'] = EVENT_POST['start_time'].from_str(data['start_time'])
        data['end_time'] = EVENT_POST['end_time'].from_str(data['end_time'])
        data['closing_datetime'] = EVENT_POST['closing_datetime'].from_str(
            data['closing_datetime'])
        data['schedule_published_on'] = EVENT_POST['schedule_published_on'].from_str(
            data['schedule_published_on'])
        return data

    def create(self, data, url):
        data, social_links = self.validate(data)
        payload = self.fix_payload(data)
        new_event = self.model(**payload)
        new_event.creator = g.user
        save_to_db(new_event, "Event saved")
        # Bind Social Links to event
        for sl in social_links:
            del sl['id']
            handle_extra_payload(sl, SOCIAL_LINK_POST)
            link, created = get_or_create(
                SocialLinkModel,
                event_id=new_event.id,
                **sl
            )
            if not created:
                link.event_id = new_event.id
                save_to_db(link, 'Save social link')

        # set organizer
        role = Role.query.filter_by(name=ORGANIZER).first()
        uer = UsersEventsRoles(g.user, new_event, role)
        save_to_db(uer, 'UER saved')
        update_version(
            event_id=new_event.id,
            is_created=True,
            column_to_increment="event_ver"
        )
        # Return created resource with a 201 status code and its Location
        # (url) in the header.
        resource_location = url + '/' + str(new_event.id)
        return self.get(new_event.id), 201, {'Location': resource_location}

    def validate(self, data, model=None):
        # Validate Social links separately
        social_links = data.get('social_links', [])

        # Remove social links from original data
        try:
            del data['social_links']
        except KeyError:
            pass
        data = BaseDAO.validate(self, data, model)
        return data, social_links

    def update(self, event_id, data):
        data, social_links = self.validate(data)
        payload = self.fix_payload(data)
        for link in social_links:
            sl, created = get_or_create(
                SocialLinkModel,
                event_id=event_id,
                **link
            )
            if not created:
                save_to_db(sl, 'Save social link')
        return BaseDAO.update(self, event_id, payload, validate=False)


LinkDAO = SocialLinkDAO(SocialLinkModel, SOCIAL_LINK_POST)
DAO = EventDAO(EventModel, EVENT_POST)

# DEFINE PARAMS

EVENT_PARAMS = {
    'location': {
        'type': str
    },
    'contains': {
        'description': 'Contains the string in name and description',
        'type': str
    },
    'state': {
        'type': str
    },
    'privacy': {
        'type': str
    },
    'type': {
        'type': str
    },
    'topic': {
        'type': str
    },
    'sub_topic': {
        'type': str
    },
    'start_time_gt': {},
    'start_time_lt': {},
    'end_time_gt': {},
    'end_time_lt': {},
    'time_period': {
        'type': str
    }
}


# DEFINE RESOURCES


class EventResource():
    """
    Event Resource Base class
    """
    event_parser = reqparse.RequestParser()
    event_parser.add_argument('location', type=str, dest='__event_location')
    event_parser.add_argument('contains', type=str, dest='__event_contains')
    event_parser.add_argument('state', type=str)
    event_parser.add_argument('privacy', type=str)
    event_parser.add_argument('type', type=str)
    event_parser.add_argument('topic', type=str)
    event_parser.add_argument('sub_topic', type=str)
    event_parser.add_argument('start_time_gt', dest='__event_start_time_gt')
    event_parser.add_argument('start_time_lt', dest='__event_start_time_lt')
    event_parser.add_argument('end_time_gt', dest='__event_end_time_gt')
    event_parser.add_argument('end_time_lt', dest='__event_end_time_lt')
    event_parser.add_argument('time_period', type=str, dest='__event_time_period')


@api.route('/<int:event_id>')
@api.param('event_id')
@api.response(404, 'Event not found')
class Event(Resource):
    @api.doc('get_event')
    @api.marshal_with(EVENT)
    def get(self, event_id):
        """Fetch an event given its id"""
        return DAO.get(event_id)

    @requires_auth
    @api.doc('delete_event')
    @api.marshal_with(EVENT)
    def delete(self, event_id):
        """Delete an event given its id"""
        event = DAO.delete(event_id)
        record_activity('delete_event', event_id=event_id)
        return event

    @requires_auth
    @api.doc('update_event', responses=PUT_RESPONSES)
    @api.marshal_with(EVENT)
    @api.expect(EVENT_POST)
    def put(self, event_id):
        """Update a event given its id"""
        event = DAO.update(event_id, self.api.payload)
        record_activity('update_event', event_id=event_id)
        return event


@api.route('')
class EventList(Resource, EventResource):
    @api.doc('list_events', params=EVENT_PARAMS)
    @api.marshal_list_with(EVENT)
    def get(self):
        """List all events"""
        return DAO.list(**parse_args(self.event_parser))

    @requires_auth
    @api.doc('create_event', responses=POST_RESPONSES)
    @api.marshal_with(EVENT)
    @api.expect(EVENT_POST)
    def post(self):
        """Create an event"""
        item = DAO.create(self.api.payload, self.api.url_for(self))
        record_activity('create_event', event_id=item[0].id)
        return item


@api.route('/page')
class EventListPaginated(Resource, PaginatedResourceBase, EventResource):
    @api.doc('list_events_paginated', params=PAGE_PARAMS)
    @api.doc(params=EVENT_PARAMS)
    @api.marshal_with(EVENT_PAGINATED)
    def get(self):
        """List events in a paginated manner"""
        args = self.parser.parse_args()
        url = self.api.url_for(self)  # WARN: undocumented way
        return get_paginated_list(
            EventModel, url, args=args,
            **parse_args(self.event_parser)
        )
