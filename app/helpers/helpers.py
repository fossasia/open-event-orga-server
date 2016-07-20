"""Copyright 2015 Rafal Kowalski"""
import json
import os
import re
import requests
from datetime import datetime, timedelta
from flask import request, url_for, current_app
from itsdangerous import Serializer
from flask.ext import login

from app.helpers.flask_helpers import get_real_ip
from app.settings import get_settings
from ..models.track import Track
from ..models.mail import INVITE_PAPERS, NEW_SESSION, USER_CONFIRM, NEXT_EVENT, \
    USER_REGISTER, PASSWORD_RESET, SESSION_ACCEPT_REJECT, SESSION_SCHEDULE, EVENT_ROLE, EVENT_PUBLISH, Mail, AFTER_EVENT
from system_mails import MAILS
from app.models.notifications import (
    # Prepended with `NOTIF_` to differentiate from mails
    EVENT_ROLE_INVITE as NOTIF_EVENT_ROLE,
    NEW_SESSION as NOTIF_NEW_SESSION,
    SESSION_SCHEDULE as NOTIF_SESSION_SCHEDULE,
    NEXT_EVENT as NOTIF_NEXT_EVENT,
    SESSION_ACCEPT_REJECT as NOTIF_SESSION_ACCEPT_REJECT,
    INVITE_PAPERS as NOTIF_INVITE_PAPERS,
)
from system_notifications import NOTIFS


def get_event_id():
    """Get event Id from request url"""
    url = request.url
    result = re.search('event\/[0-9]*', url)
    return result.group(0).split('/')[1]


def is_track_name_unique_in_event(form, event_id, *args):
    """Check unique of track name in event"""
    track_name = form.name.data
    track_id = args[0] if len(args) else None
    tracks = Track.query.filter_by(event_id=event_id, name=track_name)
    if not track_id:
        return tracks.count() == 0
    else:
        for track in tracks.all():
            return str(track.id) == track_id
        return True


#########
# Mails #
#########

def send_email_invitation(email, event_name, link):
    """Send email for submit papers"""
    send_email(
        to=email,
        action=INVITE_PAPERS,
        subject=MAILS[INVITE_PAPERS]['subject'].format(event_name=event_name),
        html=MAILS[INVITE_PAPERS]['message'].format(
            email=str(email),
            event_name=str(event_name),
            link=link
        )
    )


def send_new_session_organizer(email, event_name, link):
    """Send email after new sesions proposal"""
    send_email(
        to=email,
        action=NEW_SESSION,
        subject=MAILS[NEW_SESSION]['subject'].format(event_name=event_name),
        html=MAILS[NEW_SESSION]['message'].format(
            email=str(email),
            event_name=str(event_name),
            link=link
        )
    )


def send_session_accept_reject(email, session_name, acceptance, link):
    """Send session accepted or rejected"""
    send_email(
        to=email,
        action=SESSION_ACCEPT_REJECT,
        subject=MAILS[SESSION_ACCEPT_REJECT]['subject'].format(session_name=session_name, acceptance=acceptance),
        html=MAILS[SESSION_ACCEPT_REJECT]['message'].format(
            email=str(email),
            session_name=str(session_name),
            acceptance=str(acceptance),
            link=link
        )
    )


def send_schedule_change(email, session_name, link):
    """Send schedule change in session"""
    send_email(
        to=email,
        action=SESSION_SCHEDULE,
        subject=MAILS[SESSION_SCHEDULE]['subject'].format(session_name=session_name),
        html=MAILS[SESSION_SCHEDULE]['message'].format(
            email=str(email),
            session_name=str(session_name),
            link=link
        )
    )


def send_next_event(email, event_name, link, up_coming_events):
    """Send next event"""
    upcoming_event_html = "<ul>"
    for event in up_coming_events:
        upcoming_event_html += "<a href='%s'><li> %s </li></a>" % (url_for('events.details_view',
                                                                   event_id=event.id, _external=True),
                                                                   event.name)
    upcoming_event_html += "</ul><br/>"
    send_email(
        to=email,
        action=NEXT_EVENT,
        subject=MAILS[NEXT_EVENT]['subject'].format(event_name=event_name),
        html=MAILS[NEXT_EVENT]['message'].format(
            email=str(email),
            event_name=str(event_name),
            link=link,
            up_coming_events=upcoming_event_html
        )
    )

def send_after_event(email, event_name, upcoming_events, link=None):
    """Send after event mail"""
    upcoming_event_html = "<ul>"
    for event in upcoming_events:
        upcoming_event_html += "<a href='%s'><li> %s </li></a>" % (url_for('events.details_view',
                                                                           event_id=event.id, _external=True),
                                                                   event.name)
    upcoming_event_html += "</ul><br/>"
    send_email(
        to=email,
        action=AFTER_EVENT,
        subject=MAILS[AFTER_EVENT]['subject'].format(event_name=event_name),
        html=MAILS[AFTER_EVENT]['message'].format(
            email=str(email),
            event_name=str(event_name),
            link=link,
            up_coming_events=upcoming_event_html
        )
    )

def send_event_publish(email, event_name, link):
    """Send email on publishing event"""
    send_email(
        to=email,
        action=NEXT_EVENT,
        subject=MAILS[EVENT_PUBLISH]['subject'].format(event_name=event_name),
        html=MAILS[EVENT_PUBLISH]['message'].format(
            email=str(email),
            event_name=str(event_name),
            link=link
        )
    )


def send_email_after_account_create(form):
    """Send email after account create"""
    send_email(
        to=form['email'],
        action=USER_REGISTER,
        subject=MAILS[USER_REGISTER]['subject'],
        html=MAILS[USER_REGISTER]['message'].format(email=form['email'])
    )


def send_email_confirmation(form, link):
    """account confirmation"""
    print form
    send_email(
        to=form['email'],
        action=USER_CONFIRM,
        subject=MAILS[USER_CONFIRM]['subject'],
        html=MAILS[USER_CONFIRM]['message'].format(
            email=form['email'], link=link
        )
    )


def send_email_with_reset_password_hash(email, link):
    """Send email with reset password hash"""
    send_email(
        to=email,
        action=PASSWORD_RESET,
        subject=MAILS[PASSWORD_RESET]['subject'],
        html=MAILS[PASSWORD_RESET]['message'].format(link=link)
    )


def send_email_for_event_role_invite(email, role, event, link):
    """
    Send Email to users for Event Role invites.
    """
    subject = MAILS[EVENT_ROLE]['subject'].format(role=role, event=event)
    message = MAILS[EVENT_ROLE]['message'].format(
        email=email,
        role=role,
        event=event,
        link=link
    )
    send_email(
        to=email,
        action=EVENT_ROLE,
        subject=subject,
        html=message
    )


def send_email(to, action, subject, html):
    """
    Sends email and records it in DB
    """
    if not string_empty(to):
        key = get_settings()['sendgrid_key']
        if not key and not current_app.config['TESTING']:
            print 'Sendgrid key not defined'
            return

        if not current_app.config['TESTING']:
            headers = {
                "Authorization": ("Bearer " + key)
            }
            payload = {
                'to': to,
                'from': 'open-event@googlegroups.com',
                'subject': subject,
                'html': html
            }
            requests.post("https://api.sendgrid.com/api/mail.send.json",
                          data=payload,
                          headers=headers)
        # record_mail(to, action, subject, html)
        mail = Mail(
            recipient=to, action=action, subject=subject,
            message=html, time=datetime.now()
        )
        from data import save_to_db
        save_to_db(mail, 'Mail Recorded')
    return

#################
# Notifications #
#################

def send_notification(user, action, title, message):
    # DataManager imported here to prevent circular dependency
    from app.helpers.data import DataManager
    DataManager.create_user_notification(user, action, title, message)


def send_notif_event_role(user, role_name, event_name, accept_link, decline_link):
    notif = NOTIFS[NOTIF_EVENT_ROLE]
    action = NOTIF_EVENT_ROLE
    title = notif['title'].format(
        role_name=role_name,
        event_name=event_name
    )
    message = notif['message'].format(
        role_name=role_name,
        event_name=event_name,
        accept_link=accept_link,
        decline_link=decline_link
    )

    send_notification(user, action, title, message)


def send_notif_new_session_organizer(user, event_name, link):
    notif = NOTIFS[NOTIF_NEW_SESSION]
    action = NOTIF_NEW_SESSION
    title = notif['title'].format(event_name=event_name)
    message = notif['message'].format(event_name=event_name, link=link)

    send_notification(user, action, title, message)


def send_notif_session_schedule(user, session_name, link):
    notif = NOTIFS[NOTIF_SESSION_SCHEDULE]
    action = NOTIF_SESSION_SCHEDULE
    title = notif['title'].format(session_name=session_name)
    message = notif['message'].format(session_name=session_name, link=link)

    send_notification(user, action, title, message)


def send_notif_next_event(user, event_name, up_coming_events, link):
    notif = NOTIFS[NOTIF_NEXT_EVENT]
    action = NOTIF_NEXT_EVENT
    title = notif['title'].format(event_name=event_name)
    message = notif['message'].format(up_coming_events=up_coming_events,
                                      link=link)

    send_notification(user, action, title, message)


def send_notif_session_accept_reject(user, session_name, acceptance,
        link):
    notif = NOTIFS[NOTIF_SESSION_ACCEPT_REJECT]
    action = NOTIF_SESSION_ACCEPT_REJECT
    title = notif['title'].format(session_name=session_name,
                                  acceptance=acceptance)
    message = notif['message'].format(
        session_name=session_name,
        acceptance=acceptance,
        link=link
    )

    send_notification(user, action, title, message)


def send_notif_invite_papers(user, event_name, cfs_link, submit_link):
    notif = NOTIFS[NOTIF_INVITE_PAPERS]
    action = NOTIF_INVITE_PAPERS
    title = notif['title'].format(event_name=event_name)
    message = notif['message'].format(
        event_name=event_name,
        cfs_link=cfs_link,
        submit_link=submit_link
    )

    send_notification(user, action, title, message)


def is_event_admin(event_id, users):
    """
    :param event_id: Event id
    :param users: User id
    :return: is user admin
    """
    is_admin = False
    for user_obj in users:
        if user_obj.user.id == login.current_user.id:
            for ass in login.current_user.events_assocs:
                if ass.event_id == int(event_id):
                    is_admin = ass.admin
                    if is_event_admin:
                        return is_admin
    return is_admin


def ensure_social_link(website, link):
    """
    converts usernames of social profiles to full profile links
    if link is username, prepend website to it else return the link
    """
    if link == '' or link is None:
        return link
    if link.find('/') != -1: # has backslash, so not a username
        return link
    else:
        return website + '/' + link


def get_serializer(secret_key=None):
    return Serializer('secret_key')


def get_latest_heroku_release():
    token = os.environ.get('API_TOKEN_HEROKU', '')
    headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": "Bearer " + token,
        "Range": "version ..; max=1, order=desc"
    }
    response = requests.get("https://api.heroku.com/apps/open-event/releases", headers=headers)
    try:
        return json.loads(response.text)[0]
    except:
        return []


def get_commit_info(commit_number):
    response = requests.get("https://api.github.com/repos/fossasia/open-event-orga-server/commits/" + commit_number)
    return json.loads(response.text)


def string_empty(string):
    if type(string) is not str and type(string) is not unicode:
        return False
    if string and string.strip() and string != u'' and string != u' ':
        return False
    else:
        return True


def string_not_empty(string):
    return not string_empty(string)


def fields_not_empty(obj, fields):
    for field in fields:
        if string_empty(getattr(obj, field)):
            return False
    return True

def get_request_stats():
    """
    Get IP, Browser, Platform, Version etc
    http://werkzeug.pocoo.org/docs/0.11/utils/#module-werkzeug.useragents

    Note: request.remote_addr gives the server's address if the server is behind a reverse proxy. -@niranjan94
    """
    return {
        'ip': get_real_ip(),
        'platform': request.user_agent.platform,
        'browser': request.user_agent.browser,
        'version': request.user_agent.version,
        'language': request.user_agent.language
    }


def get_date_range(day_filter):
    day_filter = day_filter.lower()  # Use lower case for match
    format = "%Y-%m-%dT%H:%M:%S"
    date_now = datetime.now()
    start, end = None, None
    if day_filter == 'all days':
        pass
    elif day_filter == 'today':
        start = date_now.replace(hour=00, minute=00)
        end = date_now.replace(hour=23, minute=59)
    elif day_filter == 'tomorrow':
        date_now += timedelta(days=1)
        start = date_now.replace(hour=00, minute=00)
        end = date_now.replace(hour=23, minute=59)
    elif day_filter == 'this week':
        weekday = date_now.weekday()
        date_now -= timedelta(days=weekday)
        start = date_now.replace(hour=00, minute=00)
        date_now += timedelta(days=6)
        end = date_now.replace(hour=23, minute=59)
    elif day_filter == 'this weekend':
        weekday = date_now.weekday()
        date_now += timedelta(days=5 - weekday)
        start = date_now.replace(hour=00, minute=00)
        date_now += timedelta(days=1)
        end = date_now.replace(hour=23, minute=59)
    elif day_filter == 'next week':
        weekday = date_now.weekday()
        date_now -= timedelta(days=weekday)
        start = date_now.replace(hour=00, minute=00)
        date_now += timedelta(days=6)
        end = date_now.replace(hour=23, minute=59)
    elif day_filter == 'this month':
        start = first_day_of_month(date_now.replace(hour=00, minute=00))
        end = last_day_of_month(date_now.replace(hour=23, minute=59))
    else:
        try:
            from_string, to_string = day_filter.split(" to ")
            start = datetime.strptime(from_string, '%m-%d-%Y').replace(hour=00, minute=00)
            end = datetime.strptime(to_string, '%m-%d-%Y').replace(hour=23, minute=59)
        except:
            start = date_now.replace(hour=00, minute=00)
            end = date_now.replace(hour=23, minute=59)
            pass
    return start.strftime(format), end.strftime(format)


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - timedelta(days=1)


def first_day_of_month(date):
    ddays = int(date.strftime("%d")) - 1
    delta = timedelta(days=ddays)
    return date - delta


def update_state(task_handle, state, result={}):
    """
    Update state of celery task
    """
    if not current_app.config.get('CELERY_ALWAYS_EAGER'):
        task_handle.update_state(
            state=state, meta=result
        )
