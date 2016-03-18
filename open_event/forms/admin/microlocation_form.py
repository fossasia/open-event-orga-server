"""Copyright 2015 Rafal Kowalski"""
from flask_wtf import Form
from wtforms import StringField, FloatField, validators, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ...helpers.data_getter import DataGetter


class MicrolocationForm(Form):
    """Microlocation form class"""
    name = StringField('Name', [validators.DataRequired()])
    latitude = FloatField('Latitude', [validators.optional()])
    longitude = FloatField('Longitude', [validators.optional()])
    floor = IntegerField('Floor', [validators.optional()])
    room = StringField('Room', [validators.optional()])
    # session = QuerySelectField(query_factory=DataGetter.get_sessions_by_event_id, allow_blank=True)
