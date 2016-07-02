"""Copyright 2015 Rafal Kowalski"""
import pytz
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from open_event.models.role import Role
from ..models.event import Event, EventsUsers
from ..models.session import Session
# User Notifications
from ..models.notifications import Notification
from ..models.track import Track
from ..models.invite import Invite
from ..models.speaker import Speaker
from ..models.setting import Setting
from ..models.email_notifications import EmailNotification
from ..models.sponsor import Sponsor
from ..models.microlocation import Microlocation
from ..models.users_events_roles import UsersEventsRoles
from ..models.role import Role
from ..models.role_invite import RoleInvite
from ..models.service import Service
from ..models.permission import Permission
from ..models.user import User
from ..models.file import File
from ..models.session_type import SessionType
from ..models.social_link import SocialLink
from ..models.call_for_papers import CallForPaper
from ..models.custom_forms import CustomForms
from ..models.mail import Mail
from ..models.activity import Activity
from ..models.setting import Setting
from .language_list import LANGUAGE_LIST
from open_event.helpers.helpers import get_event_id
from flask.ext import login
from flask import flash, current_app
import datetime
from sqlalchemy import desc, asc


class DataGetter:
    @staticmethod
    def get_all_user_notifications(user):
        return Notification.query.filter_by(user=user).all()

    @staticmethod
    def get_user_notification(notification_id):
        return Notification.query.filter_by(id=notification_id).first()

    @staticmethod
    def get_invite_by_user_id(user_id):
        invite = Invite.query.filter_by(user_id=user_id)
        if invite:
            return invite.first()
        else:
            flash("Invite doesn't exist")
            return None

    @staticmethod
    def get_all_events():
        """Method return all events"""
        return Event.query.order_by(desc(Event.id)).all()

    @staticmethod
    def get_all_users_events_roles():
        """Method return all events"""
        return UsersEventsRoles.query

    @staticmethod
    def get_event_roles_for_user(user_id):
        return UsersEventsRoles.query.filter_by(user_id=user_id)

    @staticmethod
    def get_roles():
        return Role.query.all()

    @staticmethod
    def get_role_by_name(role_name):
        return Role.query.filter_by(name=role_name).first()

    @staticmethod
    def get_services():
        return Service.query.all()

    @staticmethod
    def get_permission_by_role_service(role, service):
        return Permission.query.filter_by(role=role, service=service).first()

    @staticmethod
    def get_event_role_invite(event_id, hash, **kwargs):
        return RoleInvite.query.filter_by(event_id=event_id,
                                          hash=hash, **kwargs).first()

    @staticmethod
    def get_all_owner_events():
        """Method return all owner events"""
        # return Event.query.filter_by(owner=owner_id)
        return login.current_user.events_assocs

    @staticmethod
    def get_email_notification_settings(user_id):
        return EmailNotification.query.filter_by(user_id=user_id)

    @staticmethod
    def get_email_notification_settings_by_event_id(user_id, event_id):
        return EmailNotification.query.filter_by(user_id=user_id).filter_by(event_id=event_id).first()

    @staticmethod
    def get_sessions_by_event_id(event_id):
        """
        :return: All Sessions with correct event_id
        """
        return Session.query.filter_by(event_id=event_id)

    @staticmethod
    def get_sessions_by_state(state):
        """
        :return: All Sessions with correct event_id
        """
        return Session.query.filter_by(state=state)

    @staticmethod
    def get_all_sessions():
        return Session.query.all()

    @staticmethod
    def get_tracks(event_id):
        """
        :param event_id: Event id
        :return: All Track with event id
        """
        return Track.query.filter_by(event_id=event_id)

    @staticmethod
    def get_tracks_by_event_id():
        """
        :return: All Tracks filtered by event_id
        """
        return Track.query.filter_by(event_id=get_event_id())

    @staticmethod
    def get_sessions(event_id, state='accepted'):
        """
        :param state: State of the session
        :param event_id: Event id
        :return: Return all Sessions objects with Event id
        """
        return Session.query.filter_by(
            event_id=event_id,
            state=state
        )

    @staticmethod
    def get_custom_form_elements(event_id):
        """
        :param event_id: Event id
        :return: Return json element of custom form
        """
        return CustomForms.query.filter_by(
            event_id=event_id
        ).first()

    @staticmethod
    def get_sessions_of_user_by_id(session_id, user=login.current_user):
        """
        :return: Return Sessions object with the current user as a speaker by ID
        """
        try:
            return Session.query.filter(Session.speakers.any(Speaker.user_id == user.id)).filter(
                Session.id == session_id).one()
        except MultipleResultsFound, e:
            return None
        except NoResultFound, e:
            return None

    @staticmethod
    def get_sessions_of_user(upcoming_events=True):
        """
        :return: Return all Sessions objects with the current user as a speaker
        """
        if upcoming_events:
            return Session.query.filter(Session.speakers.any(Speaker.user_id == login.current_user.id)).filter(
                Session.start_time >= datetime.datetime.now())
        else:
            return Session.query.filter(Session.speakers.any(Speaker.user_id == login.current_user.id)).filter(
                Session.start_time < datetime.datetime.now())

    @staticmethod
    def get_all_sessions_of_user(upcoming_events=True):
        """
        :return: Return all Sessions objects with the current user as a speaker
        """
        if upcoming_events:
            return Session.query.filter(Event.state != 'Completed')
        else:
            return Session.query.filter(Event.state == 'Completed')

    @staticmethod
    def get_speakers(event_id):
        """
        :param event_id: Event id
        :return: Speaker objects filter by event_id
        """
        return Speaker.query.filter_by(event_id=event_id).order_by(asc(Speaker.name))

    @staticmethod
    def get_speaker_columns():
        return Speaker.__table__.columns

    @staticmethod
    def get_sponsors(event_id):
        """
        :param event_id: Event id
        :return: All Sponsors fitered by event_id
        """
        return Sponsor.query.filter_by(event_id=event_id)

    @staticmethod
    def get_microlocations(event_id):
        """
        :param event_id: Event id
        :return: All Microlocation filtered by event_id
        """
        return Microlocation.query.filter_by(event_id=event_id)

    @staticmethod
    def get_microlocations_by_event_id():
        """
        :param event_id: Event id
        :return: All Microlocation filtered by event_id
        """
        return Microlocation.query.filter_by(event_id=get_event_id())

    @staticmethod
    def get_microlocation(microlocation_id):
        """
        :param microlocation_id: Microlocation id
        :return: Microlocation with microlocation_id
        """
        return Microlocation.query.get(microlocation_id)

    @staticmethod
    def get_event_owner(event_id):
        """
        :param event_id: Event id
        :return: Owner of proper event
        """
        owner_id = Event.query.get(event_id).owner
        return User.query.get(owner_id).login

    @staticmethod
    def get_all_files_tuple():
        """
        :return All files filtered by owner, Format [(test.png, test1.png)...]:
        """
        files = File.query.filter_by(owner_id=login.current_user.id)
        return [(file.name, file.name) for file in files]

    @staticmethod
    def get_all_owner_files():
        """
        :return: All owner files
        """
        files = File.query.filter_by(owner_id=login.current_user.id)
        return files

    @staticmethod
    def get_user_by_email(email):
        user = User.query.filter_by(email=email)
        if user:
            return user.first()
        else:
            flash("User doesn't exist")
            return None

    @staticmethod
    def get_all_users():
        """
        :return: All system users
        """
        return User.query.all()

    @staticmethod
    def get_user(id):
        """
        :return: User
        """
        return User.query.get(int(id))

    @staticmethod
    def get_association():
        """Return instance of EventUser"""
        return EventsUsers()

    @staticmethod
    def get_association_by_event_and_user(event_id, user_id):
        """Returns EventUser filtered by user_id and event_id"""
        return EventsUsers.query.filter_by(
            event_id=event_id,
            user_id=user_id).first()

    @staticmethod
    def get_object(db_model, object_id):
        return db_model.query.get(object_id)

    @staticmethod
    def get_event(event_id):
        return Event.query.get(event_id)

    @staticmethod
    def get_user_events_roles(event_id):
        return UsersEventsRoles.query.filter_by(user_id=login.current_user.id, event_id=event_id)

    @staticmethod
    def get_user_event_role(role_id):
        return UsersEventsRoles.query.get(role_id)

    @staticmethod
    def get_user_event_roles_by_role_name(event_id, role_name):
        return UsersEventsRoles.query.filter_by(event_id=event_id).filter(Role.name == role_name)

    @staticmethod
    def get_user_events():
        return Event.query.join(Event.roles, aliased=True).filter_by(user_id=login.current_user.id)

    @staticmethod
    def get_completed_events():
        events = Event.query.join(Event.roles, aliased=True).filter_by(user_id=login.current_user.id) \
            .filter(Event.state == 'Completed')
        return events

    @staticmethod
    def get_all_published_events(include_private=False):
        if include_private:
            events = Event.query.filter(Event.state == 'Published')
        else:
            events = Event.query.filter(Event.state == 'Published').filter(Event.privacy != 'private')
        events = events.filter(Event.start_time >= datetime.datetime.now()).filter(Event.end_time >= datetime.datetime.now())
        return events

    @staticmethod
    def get_call_for_speakers_events(include_private=False):
        if include_private:
            events = Event.query.filter(Event.state == 'Call for papers')
        else:
            events = Event.query.filter(Event.state == 'Call for papers').filter(Event.privacy != 'private')
        return events

    @staticmethod
    def get_published_events():
        events = Event.query.join(Event.roles, aliased=True).filter_by(user_id=login.current_user.id) \
            .filter(Event.state == 'Call for papers')
        return events

    @staticmethod
    def get_current_events():
        events = Event.query.join(Event.roles, aliased=True).filter_by(user_id=login.current_user.id) \
            .filter(Event.state != 'Completed')
        return events

    @staticmethod
    def get_live_events():
        return Event.query.join(Event.roles, aliased=True).filter_by(user_id=login.current_user.id)\
            .filter(Event.start_time >= datetime.datetime.now()).filter(Event.end_time >= datetime.datetime.now()) \
            .filter(Event.state == 'Published').filter(Event.in_trash == False)

    @staticmethod
    def get_draft_events():
        return Event.query.join(Event.roles, aliased=True).filter_by(user_id=login.current_user.id)\
            .filter(Event.state == 'Draft').filter(Event.in_trash == False)

    @staticmethod
    def get_past_events():
        return Event.query.join(Event.roles, aliased=True).filter_by(user_id=login.current_user.id)\
            .filter(Event.end_time <= datetime.datetime.now()).filter(Event.state == 'Published')

    @staticmethod
    def get_all_live_events():
        return Event.query.filter(Event.start_time >= datetime.datetime.now())\
            .filter(Event.end_time >= datetime.datetime.now()) \
            .filter(Event.state == 'Published')

    @staticmethod
    def get_all_draft_events():
        return Event.query.filter(Event.state == 'Draft')

    @staticmethod
    def get_all_past_events():
        return Event.query.filter(Event.end_time <= datetime.datetime.now()).filter(Event.state == 'Published')

    @staticmethod
    def get_session(session_id):
        """Get session by id"""
        return Session.query.get(session_id)

    @staticmethod
    def get_session_columns():
        return Session.__table__.columns

    @staticmethod
    def get_speaker(speaker_id):
        """Get speaker by id"""
        return Speaker.query.get(speaker_id)

    @staticmethod
    def get_speaker_by_email(email_id):
        """Get speaker by id"""
        return Speaker.query.filter_by(email=email_id)

    @staticmethod
    def get_session_types_by_event_id(event_id):
        """
        :param event_id: Event id
        :return: All Tracks filtered by event_id
        """
        return SessionType.query.filter_by(event_id=event_id)

    @staticmethod
    def get_social_links_by_event_id(event_id):
        """
        :param event_id: Event id
        :return: All Tracks filtered by event_id
        """
        return SocialLink.query.filter_by(event_id=event_id)

    @staticmethod
    def get_user_sessions():
        return Session.query.all()

    @staticmethod
    def get_call_for_papers(event_id):
        return CallForPaper.query.filter_by(event_id=event_id)

    @staticmethod
    def get_sponsor_types(event_id):
        return list(set(
            sponsor.sponsor_type for sponsor in
            Sponsor.query.filter_by(event_id=event_id)
            if sponsor.sponsor_type
        ))

    @staticmethod
    def get_event_types():
        return ['Appearance or Signing',
                'Attraction',
                'Camp, Trip, or Retreat',
                'Class, Training, or Workshop',
                'Concert or Performance',
                'Conference',
                'Convention',
                'Dinner or Gala',
                'Festival or Fair',
                'Game or Competition',
                'Meeting or Networking Event',
                'Other',
                'Party or Social Gathering',
                'Race or Endurance Event',
                'Rally',
                'Screening',
                'Seminar or Talk',
                'Tour',
                'Tournament',
                'Tradeshow, Consumer Show, or Expo']

    @staticmethod
    def get_language_list():
        return [i[1] for i in LANGUAGE_LIST]

    @staticmethod
    def get_event_topics():
        return ['Auto, Boat & Air',
                'Business & Professional',
                'Charity & Causes',
                'Community & Culture',
                'Family & Education',
                'Fashion & Beauty',
                'Film, Media & Entertainment',
                'Food & Drink',
                'Government & Politics',
                'Health & Wellness',
                'Hobbies & Special Interest',
                'Home & Lifestyle',
                'Music',
                'Other',
                'Performing & Visual Arts',
                'Religion & Spirituality',
                'Science & Technology',
                'Seasonal & Holiday',
                'Sports & Fitness',
                'Travel & Outdoor']

    @staticmethod
    def get_all_mails(count=300):
        """
        Get All Mails by latest first
        """
        mails = Mail.query.order_by(desc(Mail.time)).all()
        return mails[:count]

    @staticmethod
    def get_all_timezones():
        """
        Get all available timezones
        :return:
        """
        return [(item, "(UTC" + datetime.datetime.now(pytz.timezone(item)).strftime('%z') + ") " + item) for item
                in
                pytz.common_timezones]

    @staticmethod
    def get_sponsor(sponsor_id):
        return Sponsor.query.get(sponsor_id)

    @staticmethod
    def get_all_activities(count=300):
        """
        Get all activities by recent first
        """
        activities = Activity.query.order_by(desc(Activity.time)).all()
        return activities[:count]

    @staticmethod
    def get_trash_events():
        return Event.query.filter_by(in_trash=True)

    @staticmethod
    def get_trash_users():
        return User.query.filter_by(in_trash=True)

    @staticmethod
    def get_active_users():
        return User.query.filter_by(in_trash=False)

    @staticmethod
    def get_trash_sessions():
        return Session.query.filter_by(in_trash=True)

    @staticmethod
    def get_upcoming_events(event_id):
        up_coming_events = []
        events = DataGetter.get_all_events()
        relative_event = DataGetter.get_event(event_id)
        for event in events:
            if event.start_time >= relative_event.start_time:
                up_coming_events.append(event.name)

        return up_coming_events


