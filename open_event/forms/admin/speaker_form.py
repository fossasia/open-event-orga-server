"""Copyright 2015 Rafal Kowalski"""
from flask_wtf import Form
from flask_admin.form.widgets import Select2Widget
from wtforms import StringField, TextAreaField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from open_event.models.session import Session
from ...helpers.helpers import get_event_id


def get_sessions():
    """Returns Event's Sessions"""
    return Session.query.filter_by(event_id=get_event_id())


class SpeakerForm(Form):
    """Speaker Form class"""
    name = StringField('Name', [validators.DataRequired()])
    photo = StringField('Photo')
    biography = TextAreaField('Biography')
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    web = StringField('Web')
    twitter = StringField('Twitter')
    facebook = StringField('Facebook')
    github = StringField('Github')
    linkedin = StringField('Linkedin')
    organisation = StringField('Organisation', [validators.DataRequired()])
    position = StringField('Position')
    country = StringField('Country', [validators.DataRequired()])
    sessions = QuerySelectMultipleField(
            query_factory=get_sessions,
            widget=Select2Widget(multiple=True)
    )
