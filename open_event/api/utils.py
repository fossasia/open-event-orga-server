from flask_restplus import Model, fields, reqparse
from .helpers import get_object_list, get_object_or_404, get_object_in_event, \
    create_service_model, delete_service_model, update_model
from open_event.models.event import Event as EventModel

DEFAULT_PAGE_START = 1
DEFAULT_PAGE_LIMIT = 20

POST_RESPONSES = {401: 'Authentication failure', 400: 'Validation error'}
PUT_RESPONSES = {
    400: 'Validation Error / Bad request',
    401: 'Authentication failure',
    404: 'Object/Event not found'
}

# Parameters for a paginated response
PAGE_PARAMS = {
    'start': {
        'description': 'Serial number to start from',
        'type': int,
        'default': DEFAULT_PAGE_START
    },
    'limit': {
        'description': 'Limit on the number of results',
        'type': int,
        'default': DEFAULT_PAGE_LIMIT
    },
}

# Base Api Model for a paginated response
PAGINATED_MODEL = Model('PaginatedModel', {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'next': fields.String,
    'previous': fields.String
})


# Base class for Paginated Resource
class PaginatedResourceBase():
    """
    Paginated Resource Helper class
    This includes basic properties used in the class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('start', type=int, default=DEFAULT_PAGE_START)
    parser.add_argument('limit', type=int, default=DEFAULT_PAGE_LIMIT)


# DAO for Service Models
class ServiceDAO:
    """
    Data Access Object for service models like microlocations,
    speakers and so.
    """
    def __init__(self, model):
        self.model = model

    def get(self, event_id, sid):
        return get_object_in_event(self.model, sid, event_id)

    def list(self, event_id):
        # Check if an event with `event_id` exists
        get_object_or_404(EventModel, event_id)
        return get_object_list(self.model, event_id=event_id)

    def create(self, event_id, data):
        item = create_service_model(self.model, event_id, data)
        return item

    def update(self, event_id, service_id, data):
        item = update_model(self.model, service_id, data, event_id)
        return item

    def delete(self, event_id, service_id):
        item = delete_service_model(self.model, event_id, service_id)
        return item
