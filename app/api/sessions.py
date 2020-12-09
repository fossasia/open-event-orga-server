from typing import Dict

from flask import Blueprint, g, jsonify, request
from flask_jwt_extended import current_user
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from flask_rest_jsonapi.querystring import QueryStringManager as QSManager

from app.api.bootstrap import api
from app.api.custom_forms import CustomForms
from app.api.events import Event
from app.api.helpers.custom_forms import validate_custom_form_constraints_request
from app.api.helpers.db import get_count, safe_query, safe_query_kwargs, save_to_db
from app.api.helpers.errors import ForbiddenError, UnprocessableEntityError
from app.api.helpers.mail import send_email_new_session, send_email_session_state_change
from app.api.helpers.notification import (
    send_notif_new_session_organizer,
    send_notif_session_state_change,
)
from app.api.helpers.permission_manager import has_access, is_logged_in
from app.api.helpers.query import event_query
from app.api.helpers.speaker import can_edit_after_cfs_ends
from app.api.helpers.system_mails import MAILS, SESSION_STATE_CHANGE
from app.api.helpers.utilities import require_relationship
from app.api.schema.sessions import SessionNotifySchema, SessionSchema
from app.models import db
from app.models.microlocation import Microlocation
from app.models.session import Session
from app.models.session_speaker_link import SessionsSpeakersLink
from app.models.session_type import SessionType
from app.models.speaker import Speaker
from app.models.track import Track
from app.models.user import User

sessions_blueprint = Blueprint('sessions_blueprint', __name__, url_prefix='/v1/sessions')


class SessionListPost(ResourceList):
    """
    List Sessions
    """

    def before_post(self, args, kwargs, data):
        """
        before post method to check for required relationship and proper permission
        :param args:
        :param kwargs:
        :param data:
        :return:
        """
        require_relationship(['event', 'track'], data)
        data['creator_id'] = current_user.id
        if (
            get_count(
                db.session.query(Event).filter_by(
                    id=int(data['event']), is_sessions_speakers_enabled=False
                )
            )
            > 0
        ):
            raise ForbiddenError({'pointer': ''}, "Sessions are disabled for this Event")

        excluded = ['track']
        
        custom_fields = db.session.query(CustomForms).filter_by(event_id = data['event']).all()
        for i in custom_fields:
            if(i.field_identifier == "track" and i.is_required == True):
                excluded = []
                
        data['complex_field_values'] = validate_custom_form_constraints_request(
            'session', self.schema, Session(event_id=data['event']), data, excluded
        )

    def after_create_object(self, session, data, view_kwargs):
        """
        method to send email for creation of new session
        mails session link to the concerned user
        :param session:
        :param data:
        :param view_kwargs:
        :return:
        """
        if session.event.get_owner():
            event_name = session.event.name
            owner = session.event.get_owner()
            owner_email = owner.email
            send_email_new_session(owner_email, event_name, session.site_link)
            send_notif_new_session_organizer(
                owner, event_name, session.site_link, session.id
            )

        for speaker in session.speakers:
            session_speaker_link = SessionsSpeakersLink(
                session_state=session.state,
                session_id=session.id,
                event_id=session.event.id,
                speaker_id=speaker.id,
            )
            save_to_db(session_speaker_link, "Session Speaker Link Saved")

    decorators = (api.has_permission('create_event'),)
    schema = SessionSchema
    data_layer = {
        'session': db.session,
        'model': Session,
        'methods': {'after_create_object': after_create_object},
    }


def get_distinct_sort_fields(schema, model, sort=True):
    """Due to the poor code of flask-rest-jsonapi, distinct query needed
    in sessions API to remove duplicate sessions can't be sorted on
    returning subquery, thus we need to add all sort fields in distinct
    group and repeat it in sort group as well"""
    fields = []
    qs = QSManager(request.args, schema)
    for sort_opt in qs.sorting:
        field = sort_opt['field']
        if not hasattr(model, field):
            continue
        field = getattr(model, field)
        if sort:
            field = getattr(field, sort_opt['order'])()
        fields.append(field)
    field = Session.id
    if sort:
        field = field.desc()
    fields.append(field)
    return fields


class SessionList(ResourceList):
    """
    List Sessions
    """

    def query(self, view_kwargs):
        """
        query method for SessionList class
        :param view_kwargs:
        :return:
        """
        query_ = self.session.query(Session)
        if view_kwargs.get('track_id'):
            track = safe_query_kwargs(Track, view_kwargs, 'track_id')
            query_ = query_.join(Track).filter(Track.id == track.id)
        elif view_kwargs.get('session_type_id'):
            session_type = safe_query_kwargs(SessionType, view_kwargs, 'session_type_id')
            query_ = query_.join(SessionType).filter(SessionType.id == session_type.id)
        elif view_kwargs.get('microlocation_id'):
            microlocation = safe_query_kwargs(
                Microlocation,
                view_kwargs,
                'microlocation_id',
            )
            query_ = query_.join(Microlocation).filter(
                Microlocation.id == microlocation.id
            )
        elif view_kwargs.get('user_id'):
            user = safe_query_kwargs(User, view_kwargs, 'user_id')
            query_ = (
                query_.join(User)
                .join(Speaker)
                .filter(
                    User.id == user.id or Session.speakers.any(Speaker.user_id == user.id)
                )
                .distinct(*get_distinct_sort_fields(SessionSchema, Session, sort=False))
                .order_by(*get_distinct_sort_fields(SessionSchema, Session))
            )
        elif view_kwargs.get('speaker_id'):
            speaker = safe_query_kwargs(Speaker, view_kwargs, 'speaker_id')
            # session-speaker :: many-to-many relationship
            query_ = Session.query.filter(Session.speakers.any(id=speaker.id))
        elif view_kwargs.get('event_id') or view_kwargs.get('event_identifier'):
            query_ = event_query(query_, view_kwargs)

        return query_

    view_kwargs = True
    methods = ['GET']
    schema = SessionSchema
    data_layer = {'session': db.session, 'model': Session, 'methods': {'query': query}}


SESSION_STATE_DICT = {
    'organizer': {
        'draft': {},  # No state change allowed
        'pending': {
            'withdrawn': True,
            'accepted': True,
            'rejected': True,
            'confirmed': True,
        },
        'accepted': {
            'withdrawn': True,
            'rejected': True,
            'confirmed': True,
            'canceled': True,
        },
        'confirmed': {
            'withdrawn': True,
            'accepted': True,
            'rejected': True,
            'canceled': True,
        },
        'rejected': {'withdrawn': True, 'accepted': True, 'confirmed': True},
        'canceled': {
            'withdrawn': True,
            'accepted': True,
            'rejected': True,
            'confirmed': True,
        },
        'withdrawn': {},  # Withdrawn is final
    },
    'speaker': {
        'draft': {'pending': True},
        'pending': {'withdrawn': True},
        'accepted': {'withdrawn': True},
        'confirmed': {'withdrawn': True},
        'rejected': {'withdrawn': True},
        'canceled': {'withdrawn': True},
        'withdrawn': {},  # Withdrawn is final
    },
}


@sessions_blueprint.route('/states')
def get_session_states():
    return jsonify(SESSION_STATE_DICT)


@sessions_blueprint.route('/mails')
def get_session_state_change_mails():
    return jsonify(MAILS[SESSION_STATE_CHANGE])


class SessionDetail(ResourceDetail):
    """
    Session detail by id
    """

    def before_get_object(self, view_kwargs):
        """
        before get method to get the resource id for fetching details
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('event_identifier'):
            event = safe_query(
                Event, 'identifier', view_kwargs['event_identifier'], 'identifier'
            )
            view_kwargs['event_id'] = event.id

    def after_get_object(self, session, view_kwargs):
        is_speaker_or_admin = is_logged_in() and has_access(
            'is_speaker_for_session', id=session.id
        )
        if session.state not in ['accepted', 'confirmed'] and not is_speaker_or_admin:
            raise ObjectNotFound({'parameter': '{id}'}, "Session: not found")

    def before_update_object(self, session, data, view_kwargs):
        """
        before update method to verify if session is locked before updating session object
        :param event:
        :param data:
        :param view_kwargs:
        :return:
        """
        is_organizer = has_access('is_admin') or has_access(
            'is_organizer', event_id=session.event_id
        )
        if session.is_locked and not is_organizer:
            raise ForbiddenError(
                {'pointer': '/data/attributes/is-locked'},
                "Locked sessions cannot be edited",
            )

        new_state = data.get('state')

        if new_state and new_state != session.state:
            # State change detected. Verify that state change is allowed
            g.send_email = new_state in [
                'accepted',
                'rejected',
                'confirmed',
                'rejected',
                'canceled',
                'withdrawn',
            ]
            key = 'speaker'
            if is_organizer:
                key = 'organizer'
            state_dict = SESSION_STATE_DICT[key]
            try:
                state_dict[session.state][new_state]
            except KeyError:
                raise ForbiddenError(
                    {'pointer': '/data/attributes/state'},
                    f'You cannot change a session state from "{session.state}" to "{new_state}"',
                )

        if not can_edit_after_cfs_ends(session.event_id):
            raise ForbiddenError(
                {'source': ''}, "Cannot edit session after the call for speaker is ended"
            )

        # We allow organizers and admins to edit session without validations
        complex_field_values = data.get('complex_field_values', 'absent')
        # Set default to 'absent' to differentiate between None and not sent
        is_absent = complex_field_values == 'absent'
        # True if values are not sent in data JSON
        is_same = data.get('complex_field_values') == session.complex_field_values
        # Using original value to ensure None instead of absent
        # We stop checking validations for organizers only if they may result in data change or absent. See test_session_forms_api.py for more info
        if not (is_organizer and (is_absent or is_same)):
            data['complex_field_values'] = validate_custom_form_constraints_request(
                'session', self.resource.schema, session, data
            )

    def after_update_object(self, session, data, view_kwargs):
        """ Send email if session accepted or rejected """

        if data.get('send_email', None) and g.get('send_email'):
            notify_for_session(session)

        if 'state' in data:
            entry_count = SessionsSpeakersLink.query.filter_by(session_id=session.id)
            if entry_count.count() == 0:
                is_patch_request = False
            else:
                is_patch_request = True

            if is_patch_request:
                for focus_session in entry_count:
                    focus_session.session_state = session.state
                db.session.commit()
            else:
                current_session = Session.query.filter_by(id=session.id).first()
                for speaker in current_session.speakers:
                    session_speaker_link = SessionsSpeakersLink(
                        session_state=session.state,
                        session_id=session.id,
                        event_id=session.event.id,
                        speaker_id=speaker.id,
                    )
                    save_to_db(session_speaker_link, "Session Speaker Link Saved")

    decorators = (api.has_permission('is_speaker_for_session', methods="PATCH,DELETE"),)
    schema = SessionSchema
    data_layer = {
        'session': db.session,
        'model': Session,
        'methods': {
            'before_update_object': before_update_object,
            'before_get_object': before_get_object,
            'after_update_object': after_update_object,
            'after_get_object': after_get_object,
        },
    }


def notify_for_session(session, mail_override: Dict[str, str] = None):
    # Email for speaker
    speakers = session.speakers
    for speaker in speakers:
        if not speaker.is_email_overridden:
            send_email_session_state_change(speaker.email, session, mail_override)
            send_notif_session_state_change(
                speaker.user, session.title, session.state, session.site_link, session.id
            )

    # Email for owner
    if session.event.get_owner():
        owner = session.event.get_owner()
        send_email_session_state_change(owner.email, session, mail_override)
        send_notif_session_state_change(
            owner, session.title, session.state, session.site_link, session.id
        )


@sessions_blueprint.route('/<int:id>/notify', methods=['POST'])
@api.has_permission('is_speaker_for_session', methods="POST")
def notify_session(id):
    session = Session.query.filter_by(deleted_at=None, id=id).first_or_404()

    data, errors = SessionNotifySchema().load(request.json)
    if errors:
        raise UnprocessableEntityError(
            {'pointer': '/data', 'errors': errors}, 'Data in incorrect format'
        )

    notify_for_session(session, data)

    return jsonify({'success': True})


class SessionRelationshipRequired(ResourceRelationship):
    """
    Session Relationship
    """

    schema = SessionSchema
    decorators = (api.has_permission('is_speaker_for_session', methods="PATCH,DELETE"),)
    methods = ['GET', 'PATCH']
    data_layer = {'session': db.session, 'model': Session}


class SessionRelationshipOptional(ResourceRelationship):
    """
    Session Relationship
    """

    schema = SessionSchema
    decorators = (api.has_permission('is_speaker_for_session', methods="PATCH,DELETE"),)
    data_layer = {'session': db.session, 'model': Session}
