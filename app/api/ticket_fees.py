from app.api.bootstrap import api
from flask_rest_jsonapi import ResourceDetail, ResourceList
from marshmallow import validate
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields

from app import db
from app.api.helpers.static import PAYMENT_CURRENCY_CHOICES
from app.api.helpers.utilities import dasherize
from app.models.ticket_fee import TicketFees


class TicketFeesSchema(Schema):
    """
    Api schema for ticket_fee Model
    """
    class Meta:
        """
        Meta class for image_size Api Schema
        """
        type_ = 'ticket-fees'
        self_view = 'v1.ticket_fee_detail'
        self_view_kwargs = {'id': '<id>'}
        inflect = dasherize

    id = fields.Integer(dump_only=True)
    currency = fields.Str(validate=validate.OneOf(choices=PAYMENT_CURRENCY_CHOICES), allow_none=True)
    service_fee = fields.Float(validate=lambda n: n >= 0, allow_none=True)
    maximum_fee = fields.Float(validate=lambda n: n >= 0, allow_none=True)


class TicketFeeList(ResourceList):
    """
    List and create TicketFees
    """
    decorators = (api.has_permission('is_admin'),)
    schema = TicketFeesSchema
    data_layer = {'session': db.session,
                  'model': TicketFees}


class TicketFeeDetail(ResourceDetail):
    """
    ticket_fee detail by id
    """
    decorators = (api.has_permission('is_admin'),)
    schema = TicketFeesSchema
    data_layer = {'session': db.session,
                  'model': TicketFees}
