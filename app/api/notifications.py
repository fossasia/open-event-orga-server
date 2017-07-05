from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

from app.api.helpers.utilities import dasherize
from app.models import db
from app.models.notification import Notification
from app.models.user import User
from app.api.helpers.permissions import is_user_itself, jwt_required
from app.api.helpers.db import safe_query


class NotificationSchema(Schema):
    """
    API Schema for Notification Model
    """

    class Meta:
        """
        Meta class for Notification API schema
        """
        type_ = 'notification'
        self_view = 'v1.notification_detail'
        self_view_kwargs = {'id': '<id>'}
        inflect = dasherize

    id = fields.Str(dump_only=True)
    title = fields.Str()
    message = fields.Str()
    received_at = fields.DateTime(dump_only=True)
    accept = fields.Str()
    is_read = fields.Boolean()
    user = Relationship(attribute='user',
                        self_view='v1.notification_user',
                        self_view_kwargs={'id': '<id>'},
                        related_view='v1.user_detail',
                        related_view_kwargs={'notification_id': '<id>'},
                        schema='UserSchema',
                        type_='user'
                        )


class NotificationList(ResourceList):
    """
    List all the Notification
    """

    def query(self, view_kwargs):
        """
        query method for Notifications list
        :param view_kwargs:
        :return:
        """
        query_ = self.session.query(Notification)
        if view_kwargs.get('id'):
            user = safe_query(self, User, 'id', view_kwargs['id'], 'id')
            query_ = query_.join(User).filter(User.id == user.id)
        return query_

    def before_create_object(self, data, view_kwargs):
        """
        method to create object before post
        :param data:
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('id') is not None:
            user = safe_query(self, User, 'id', view_kwargs['id'], 'id')
            data['user_id'] = user.id

    view_kwargs = True
    decorators = (is_user_itself,)
    schema = NotificationSchema
    data_layer = {'session': db.session,
                  'model': Notification,
                  'methods': {
                      'query': query,
                      'before_create_object': before_create_object
                  }}


class NotificationDetail(ResourceDetail):
    """
    Notification detail by ID
    """
    decorators = (is_user_itself,)
    schema = NotificationSchema
    data_layer = {'session': db.session,
                  'model': Notification}


class NotificationRelationship(ResourceRelationship):
    """
    Notification Relationship
    """
    decorators = (jwt_required,)
    schema = NotificationSchema
    data_layer = {'session': db.session,
                  'model': Notification}
