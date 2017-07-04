from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
import marshmallow.validate as validate
from sqlalchemy.orm.exc import NoResultFound
from flask_rest_jsonapi.exceptions import ObjectNotFound

from app.api.helpers.utilities import dasherize
from app.api.helpers.permissions import is_admin
from app.models import db
from app.models.event import Event
from app.models.user import User
from app.models.event_invoice import EventInvoice
from app.models.discount_code import DiscountCode
from app.api.helpers.static import PAYMENT_COUNTRIES


class EventInvoiceSchema(Schema):
    """
    Event Invoice API Schema based on event invoice model
    """
    class Meta:
        type_ = 'event-invoice'
        self_view = 'v1.event_invoice_detail'
        self_view_kwargs = {'id': '<id>'}
        inflect = dasherize

    id = fields.Str(dump_only=True)
    identifier = fields.Str(allow_none=True)
    amount = fields.Float(validate=lambda n: n >= 0, allow_none=True)
    address = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    state = fields.Str(allow_none=True)
    country = fields.Str(validate=validate.OneOf(choices=PAYMENT_COUNTRIES), allow_none=True)
    zipcode = fields.Str(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    completed_at = fields.DateTime(default=None)
    transaction_id = fields.Str(allow_none=True)
    paid_via = fields.Str(validate=validate.OneOf(
        choices=["free", "stripe", "paypal", "transfer", "onsite", "cheque"]), allow_none=True)
    payment_mode = fields.Str(allow_none=True)
    brand = fields.Str(allow_none=True)
    exp_month = fields.Integer(validate=lambda n: 0 <= n <= 12, allow_none=True)
    exp_year = fields.Integer(validate=lambda n: n >= 2015, allow_none=True)
    last4 = fields.Str(allow_none=True)
    stripe_token = fields.Str(allow_none=True)
    paypal_token = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(
        choices=["expired", "deleted", "initialized" "completed", "placed", "pending", "cancelled"]), allow_none=True)
    invoice_pdf_url = fields.Url(allow_none=True)
    user = Relationship(attribute='user',
                        self_view='v1.event_invoice_user',
                        self_view_kwargs={'id': '<id>'},
                        related_view='v1.user_detail',
                        related_view_kwargs={'event_invoice_id': '<id>'},
                        schema='UserSchema',
                        type_='user')
    event = Relationship(attribute='event',
                         self_view='v1.event_invoice_event',
                         self_view_kwargs={'id': '<id>'},
                         related_view='v1.event_detail',
                         related_view_kwargs={'event_invoice_id': '<id>'},
                         schema='EventSchema',
                         type_='event')
    discount_codes = Relationship(attribute='discount_code',
                                  self_view='v1.event_invoice_discount_code',
                                  self_view_kwargs={'id': '<id>'},
                                  related_view='v1.discount_code_detail',
                                  related_view_kwargs={'event_invoice_id': '<id>'},
                                  schema='DiscountCodeSchema',
                                  type_='discount-code')


class EventInvoiceList(ResourceList):
    """
    List and Create Event Invoices
    """

    def query(self, view_kwargs):
        """
        query method for event invoice list
        :param view_kwargs:
        :return:
        """
        query_ = self.session.query(EventInvoice)
        if view_kwargs.get('event_id'):
            try:
                event = self.session.query(Event).filter_by(id=view_kwargs['event_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'event_id'},
                                     "Event: {} not found".format(view_kwargs['event_id']))
            else:
                query_ = query_.filter(Event.id == event.id)
        elif view_kwargs.get('event_identifier'):
            try:
                event = self.session.query(Event).filter_by(identifier=view_kwargs['event_identifier']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'event_identifier'},
                                     "Event: {} not found".format(view_kwargs['event_identifier']))
            else:
                query_ = query_.join(Event).filter(Event.id == event.id)
        if view_kwargs.get('user_id'):
            try:
                user = self.session.query(User).filter_by(id=view_kwargs['user_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'user_id'},
                                     "User: {} not found".format(view_kwargs['user_id']))
            else:
                query_ = query_.join(Event).filter(User.id == user.id)
        if view_kwargs.get('discount_code_id'):
            try:
                discount_code = self.session.query(DiscountCode).\
                    filter_by(discount_code_id=view_kwargs['discount_code_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'discount_code_id'},
                                     "Discount Code: {} not found".format(view_kwargs['discount_code_id']))
            else:
                query_ = query_.join(Event).filter(DiscountCode.id == discount_code.id)
        return query_

    def before_create_object(self, data, view_kwargs):
        """
        method to create object before post
        :param data:
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('event_id'):
            try:
                event = self.session.query(Event).filter_by(id=view_kwargs['event_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'event_id'},
                                     "Event: {} not found".format(view_kwargs['event_id']))
            else:
                data['event_id'] = event.id
        elif view_kwargs.get('event_identifier'):
            try:
                event = self.session.query(Event).filter_by(identifier=view_kwargs['event_identifier']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'event_identifier'},
                                     "Event: {} not found".format(view_kwargs['event_identifier']))
            else:
                data['event_id'] = event.id
        if view_kwargs.get('user_id'):
            try:
                user = self.session.query(User).filter_by(id=view_kwargs['user_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'user_id'},
                                     "User: {} not found".format(view_kwargs['user_id']))
            else:
                data['user_id'] = user.id
        if view_kwargs.get('discount_code_id'):
            try:
                discount_code = self.session.query(DiscountCode).\
                    filter_by(discount_code_id=view_kwargs['discount_code_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'discount_code_id'},
                                     "Discount Code: {} not found".format(view_kwargs['discount_code_id']))
            else:
                data['discount_code_id'] = discount_code.id

    view_kwargs = True
    decorators = (is_admin,)
    schema = EventInvoiceSchema
    data_layer = {'session': db.session,
                  'model': EventInvoice,
                  'methods': {
                      'query': query,
                      'before_create_object': before_create_object}}


class EventInvoiceDetail(ResourceDetail):
    """
    Event Invoice detail by id
    """
    decorators = (is_admin,)
    schema = EventInvoiceSchema
    data_layer = {'session': db.session,
                  'model': EventInvoice}


class EventInvoiceRelationship(ResourceRelationship):
    """
    Event Invoice Relationship
    """
    decorators = (is_admin,)
    schema = EventInvoiceSchema
    data_layer = {'session': db.session,
                  'model': EventInvoice}
