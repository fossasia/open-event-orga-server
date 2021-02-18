import pytz
from flask import jsonify
from flask_jwt_extended import current_user
from icalendar import Calendar, Event
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.models.session import Session


def to_ical(event, include_sessions=False, my_schedule=False):
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('METHOD', 'PUBLISH')
    cal.add('X-WR-CALNAME', event.name)
    cal.add('X-WR-CALDESC', 'Event Calendar')

    event_component = Event()
    event_component.add('uid', event.identifier)
    event_component.add('summary', event.name)
    event_component.add('url', event.site_link)
    event_component.add('dtstart', event.starts_at_tz)
    event_component.add('dtend', event.ends_at_tz)
    event_component.add('location', event.normalized_location)
    event_component.add('description', event.description)
    if event.has_coordinates:
        event_component.add('geo', (event.latitude, event.longitude))
    if event.owner_description:
        event_component.add('organizer', event.owner_description)

    cal.add_component(event_component)

    if include_sessions:
        sessions_query = (
            Session.query.filter_by(event_id=event.id)
            .options(joinedload(Session.microlocation))
            .filter_by(deleted_at=None)
            .filter(or_(Session.state == 'accepted', Session.state == 'confirmed'))
            .order_by(Session.starts_at.asc())
        )
        if my_schedule:
            if not current_user:
                return jsonify(error='Login Required'), 401
            sessions_query = sessions_query.join(Session.favourites).filter_by(
                user=current_user
            )
        sessions = sessions_query.all()

        for session in sessions:

            if not (session and session.starts_at and session.ends_at):
                continue

            session_component = Event()
            session_component.add('summary', session.title)
            session_component.add('uid', str(session.id) + "-" + event.identifier)
            session_component.add('geo', (event.latitude, event.longitude))
            session_component.add(
                'location',
                session.microlocation
                and session.microlocation.name
                or '' + " " + event.location_name,
            )
            session_component.add(
                'dtstart', session.starts_at.astimezone(pytz.timezone(event.timezone))
            )
            session_component.add(
                'dtend', session.ends_at.astimezone(pytz.timezone(event.timezone))
            )
            session_component.add('description', session.short_abstract)
            session_component.add('url', event.site_link + '/session/' + str(session.id))

            cal.add_component(session_component)

    return cal.to_ical()
