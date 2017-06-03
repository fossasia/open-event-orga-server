from flask import current_app as app, Blueprint
from flask_rest_jsonapi import Api

from app.api.users import UserList, UserDetail, UserRelationship
from app.api.tickets import AllTicketList, TicketDetail, TicketRelationship
from app.api.events import EventList, EventDetail, EventRelationship
from app.api.microlocations import MicrolocationList, MicrolocationDetail, MicrolocationRelationship
from app.api.sessions import SessionList, SessionDetail, SessionRelationship
from app.api.social_links import SocialLinkList, SocialLinkDetail, SocialLinkRelationship
from app.api.sponsors import SponsorList, SponsorDetail, SponsorRelationship
from app.api.tracks import TrackList, TrackDetail, TrackRelationship
from app.api.orders import OrderList, OrderDetail, OrderRelationship


api_v1 = Blueprint('v1', __name__, url_prefix='/v1')
api = Api(app, api_v1)

# users
api.route(UserList, 'user_list', '/users')
api.route(UserDetail, 'user_detail', '/users/<int:id>', '/orders/<int:order_id>/user')
api.route(UserRelationship, 'user_order', '/users/<int:id>/relationships/order')

# tickets
api.route(AllTicketList, 'all_ticket_list', '/tickets', '/events/<int:id>/tickets')
api.route(TicketDetail, 'ticket_detail', '/tickets/<int:id>')
api.route(TicketRelationship, 'ticket_event', '/tickets/<int:id>/relationships/event')

# events
api.route(EventList, 'event_list', '/events')
api.route(EventDetail, 'event_detail', '/events/<int:id>', '/tickets/<int:ticket_id>/event',
          '/microlocations/<int:microlocation_id>/event', '/social_links/<int:social_link_id>/event',
          '/sponsors/<int:sponsor_id>/event', '/tracks/<int:track_id>/event',
          '/orders/<int:order_id>/event')
api.route(EventRelationship, 'event_ticket', '/events/<int:id>/relationships/ticket')
api.route(EventRelationship, 'event_microlocation', '/events/<int:id>/relationships/microlocation')
api.route(EventRelationship, 'event_social_link', '/events/<int:id>/relationships/social_link')
api.route(EventRelationship, 'event_sponsor', '/events/<int:id>/relationships/sponsor')
api.route(EventRelationship, 'event_tracks', '/events/<int:id>/relationships/tracks')
api.route(EventRelationship, 'event_order', '/events/<int:id>/relationships/order')

# microlocations
api.route(MicrolocationList, 'microlocation_list', '/microlocations',
          '/events/<int:id>/microlocations', '/sessions/<int:id>/microlocations')
api.route(MicrolocationDetail, 'microlocation_detail', '/microlocations/<int:id>',
          '/sessions/<int:session_id>/microlocation', '/events/<int:event_id>/microlocation')
api.route(MicrolocationRelationship, 'microlocation_session',
          '/microlocations/<int:id>/relationships/session')
api.route(MicrolocationRelationship, 'microlocation_event',
          '/microlocations/<int:id>/relationships/event')

# sessions
api.route(SessionList, 'session_list', '/sessions', '/events/<int:id>/sessions', '/tracks/<int:track_id>/sessions')
api.route(SessionDetail, 'session_detail', '/sessions/<int:id>',
          '/microlocations/<int:microlocation_id>/sessions', '/events/<int:event_id>/microlocations')
api.route(SessionRelationship, 'session_microlocation',
          '/sessions/<int:id>/relationships/microlocation')
api.route(SessionRelationship, 'session_track', '/sessions/<int:id>/relationships/track')

# social_links
api.route(SocialLinkList, 'social_link_list', '/social_links', '/events/<int:id>/social_links')
api.route(SocialLinkDetail, 'social_link_detail',
          '/social_links/<int:id>', '/events/<int:event_id>/social_links')
api.route(SocialLinkRelationship, 'social_link_event',
          '/social_links/<int:id>/relationships/event')

# sponsors
api.route(SponsorList, 'sponsor_list', '/sponsors', '/events/<int:event_id>/sponsors')
api.route(SponsorDetail, 'sponsor_detail', '/sponsors/<int:id>')
api.route(SponsorRelationship, 'sponsor_event', '/sponsors/<int:id>/relationships/event')

# tracks
api.route(TrackList, 'track_list', '/tracks', '/events/<int:event_id>/tracks')
api.route(TrackDetail, 'track_detail', '/tracks/<int:id>', '/sessions/<int:session_id>/track')
api.route(TrackRelationship, 'track_sessions', '/tracks/<int:id>/relationships/sessions')
api.route(TrackRelationship, 'track_event', '/tracks/<int:id>/relationships/event')

# Orders
api.route(OrderList, 'order_list', '/orders', 
     '/events/<int:event_id>/orders', '/users/<int:user_id>/orders')
# one last option can be done as /eevnts/event_id/orders?user=[1,3] in filtering
api.route(OrderDetail, 'order_detail', '/orders/<int:id>')
api.route(OrderRelationship, 'order_event', '/orders/<int:id>/relationships/event')
api.route(OrderRelationship, 'order_user', '/orders/<int:id>/relationships/user')
