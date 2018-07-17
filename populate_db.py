from app import current_app
from app.models import db
from app.api.helpers.db import get_or_create  # , save_to_db
from envparse import env

# Admin message settings
from app.api.helpers.system_mails import MAILS
from app.models.message_setting import MessageSettings

# Event Role-Service Permissions
from app.models.role import Role
from app.models.service import Service
from app.models.permission import Permission

from app.models.track import Track
from app.models.session import Session
from app.models.speaker import Speaker
from app.models.sponsor import Sponsor
from app.models.microlocation import Microlocation

from app.models.user import ORGANIZER, COORGANIZER, TRACK_ORGANIZER, MODERATOR, ATTENDEE, REGISTRAR

# Admin Panel Permissions
from app.models.panel_permission import PanelPermission
from app.models.custom_system_role import CustomSysRole

from app.models.setting import Setting
from app.models.image_size import ImageSizes
from app.models.module import Module

# EventTopic
from app.models.event_topic import EventTopic

# EventType
from app.models.event_type import EventType

# EventLocation
from app.models.event_location import EventLocation

# User Permissions
from app.models.user_permission import UserPermission
SALES = 'sales'


def create_roles():
    get_or_create(Role, name=ORGANIZER, title_name='Organizer')
    get_or_create(Role, name=COORGANIZER, title_name='Co-organizer')
    get_or_create(Role, name=TRACK_ORGANIZER, title_name='Track Organizer')
    get_or_create(Role, name=MODERATOR, title_name='Moderator')
    get_or_create(Role, name=ATTENDEE, title_name='Attendee')
    get_or_create(Role, name=REGISTRAR, title_name='Registrar')


def create_services():
    track = Track.get_service_name()
    session = Session.get_service_name()
    speaker = Speaker.get_service_name()
    sponsor = Sponsor.get_service_name()
    microlocation = Microlocation.get_service_name()

    get_or_create(Service, name=track)
    get_or_create(Service, name=session)
    get_or_create(Service, name=speaker)
    get_or_create(Service, name=sponsor)
    get_or_create(Service, name=microlocation)


def create_settings():
    get_or_create(Setting, app_name='Open Event')

    if current_app.config['DEVELOPMENT']:
        # get the stripe keys from the env file and save it in the settings.
        env.read_envfile()
        stripe_secret_key = env('STRIPE_SECRET_KEY', default=None)
        stripe_publishable_key = env('STRIPE_PUBLISHABLE_KEY', default=None)
        stripe_client_id = env('STRIPE_CLIENT_ID', default=None)

        if stripe_client_id and stripe_secret_key and stripe_publishable_key:
            setting, _ = get_or_create(Setting, app_name='Open Event')
            setting.stripe_client_id = stripe_client_id
            setting.stripe_publishable_key = stripe_publishable_key
            setting.stripe_secret_key = stripe_secret_key
            db.session.add(setting)
            db.session.commit()


def create_event_image_sizes():
    get_or_create(
        ImageSizes, type='event-image', full_width=1300,
        full_height=500, full_aspect=True, full_quality=80,
        icon_width=75, icon_height=30, icon_aspect=True,
        icon_quality=80, thumbnail_width=500, thumbnail_height=200,
        thumbnail_aspect=True, thumbnail_quality=80, logo_width=500,
        logo_height=200
    )


def create_speaker_image_sizes():
    get_or_create(
        ImageSizes, type='speaker-image', icon_size_width_height=35, icon_size_quality=80,
        small_size_width_height=50, small_size_quality=80,
        thumbnail_size_width_height=500, thumbnail_quality=80
    )


def create_modules():
    get_or_create(Module, donation_include=False)


def create_event_topics():
    event_topic = ['Health & Wellness', 'Home & Lifestyle',
                   'Charity & Causes', 'Other', 'Religion & Spirituality',
                   'Community & Culture', 'Government & Politics',
                   'Government & Politics', 'Auto, Boat & Air',
                   'Travel & Outdoor', 'Hobbies & Special Interest',
                   'Sports & Fitness', 'Business & Professional',
                   'Music', 'Seasonal & Holiday',
                   'Film, Media & Entertainment', 'Family & Education',
                   'Science & Technology', 'Performing & Visual Arts',
                   'Food & Drink', 'Family & Education']
    for topic in event_topic:
        get_or_create(EventTopic, name=topic)


def create_event_types():
    event_type = ['Camp, Treat & Retreat', 'Dinner or Gala',
                  'Other', 'Concert or Performance', 'Conference',
                  'Seminar or Talk', 'Convention',
                  'Festival or Fair', 'Tour',
                  'Screening', 'Game or Competition',
                  'Party or Social Gathering', 'Race or Endurance Event',
                  'Meeting or Networking Event', 'Attraction',
                  'Class, Training, or Workshop', 'Appearance or Signing',
                  'Tournament', 'Rally']
    for type_ in event_type:
        get_or_create(EventType, name=type_)


def create_event_locations():
    event_location = ['India', 'Singapore', 'Berlin', 'New York', 'Hong Kong']
    for loc_ in event_location:
        get_or_create(EventLocation, name=loc_)


def create_permissions():
    orgr = Role.query.get(1)
    coorgr = Role.query.get(2)
    track_orgr = Role.query.get(3)
    mod = Role.query.get(4)
    attend = Role.query.get(5)
    regist = Role.query.get(6)

    track = Service.query.get(1)
    session = Service.query.get(2)
    speaker = Service.query.get(3)
    sponsor = Service.query.get(4)
    microlocation = Service.query.get(5)

    # For ORGANIZER
    # All four permissions set to True
    services = [track, session, speaker, sponsor, microlocation]
    roles = [attend, regist]
    for service in services:
        perm, _ = get_or_create(Permission, role=orgr, service=service)
        db.session.add(perm)

    # For COORGANIZER
    for service in services:
        perm, _ = get_or_create(Permission, role=coorgr, service=service)
        perm.can_create, perm.can_delete = False, False
        db.session.add(perm)

    # For TRACK_ORGANIZER
    for service in services:
        perm, _ = get_or_create(Permission, role=track_orgr, service=service)
        if not service == track:
            perm.can_create, perm.can_update, perm.can_delete = False, False, False
        db.session.add(perm)

    # For MODERATOR
    for service in services:
        perm, _ = get_or_create(Permission, role=mod, service=service)
        perm.can_create, perm.can_update, perm.can_delete = False, False, False
        db.session.add(perm)

    # For ATTENDEE and REGISTRAR
    services = [track, session, speaker, sponsor, microlocation]
    roles = [attend, regist]
    for role in roles:
        for service in services:
            perm, _ = get_or_create(Permission, role=role, service=service)
            perm.can_create, perm.can_update, perm.can_delete = False, False, False
            db.session.add(perm)


def create_custom_sys_roles():
    role, _ = get_or_create(CustomSysRole, name='Sales Admin')
    db.session.add(role)
    role, _ = get_or_create(CustomSysRole, name='Marketer')
    db.session.add(role)


def create_panel_permissions():
    sales_admin = CustomSysRole.query.filter_by(name='Sales Admin').first()
    perm, _ = get_or_create(PanelPermission, panel_name=SALES, role=sales_admin)
    db.session.add(perm)
    marketer = CustomSysRole.query.filter_by(name='Marketer').first()
    perm, _ = get_or_create(PanelPermission, panel_name=SALES, role=marketer)
    db.session.add(perm)


def create_user_permissions():
    # Publish Event
    user_perm, _ = get_or_create(UserPermission, name='publish_event',
                                 description='Publish event (make event live)')
    user_perm.verified_user = True
    db.session.add(user_perm)

    # Create Event
    user_perm, _ = get_or_create(UserPermission, name='create_event',
                                 description='Create event')
    user_perm.verified_user, user_perm.unverified_user = True, False
    db.session.add(user_perm)


def create_admin_message_settings():
    default_mails = ["Next Event",
                     "Session Schedule Change",
                     "User email",
                     "Invitation For Papers",
                     "After Event",
                     "Ticket(s) Purchased",
                     "Session Accept or Reject",
                     "Event Published",
                     "Event Export Failed",
                     "Event Exported",
                     "Event Role Invitation",
                     "New Session Proposal"]
    for mail in MAILS:
        if mail in default_mails:
            get_or_create(MessageSettings, action=mail, mail_status=True,
                          notification_status=True, user_control_status=True)
        else:
            get_or_create(
                MessageSettings, action=mail, mail_status=False,
                notification_status=False, user_control_status=False
            )


def populate():
    """
    Create defined Roles, Services and Permissions.
    """
    print('Creating roles...')
    create_roles()
    print('Creating services...')
    create_services()
    print('Creating permissions...')
    create_permissions()
    print('Creating custom system roles...')
    create_custom_sys_roles()
    print('Creating admin panel permissions...')
    create_panel_permissions()
    print('Creating user permissions...')
    create_user_permissions()
    print('Creating settings...')
    create_settings()
    print('Creating modules...')
    create_modules()
    print('Creating event image size...')
    create_event_image_sizes()
    print('Creating speaker image size...')
    create_speaker_image_sizes()
    print('Creating Event Topics...')
    create_event_topics()
    print('Creating Event Types...')
    create_event_types()
    print('Creating Event Locations...')
    create_event_locations()
    print('Creating admin message settings...')
    create_admin_message_settings()


def populate_without_print():
    """
    Create defined Roles, Services and Permissions.
    """
    create_roles()
    create_services()
    create_permissions()
    create_custom_sys_roles()
    create_panel_permissions()
    create_user_permissions()
    create_settings()
    create_modules()
    create_event_image_sizes()
    create_speaker_image_sizes()
    create_event_topics()
    create_event_types()
    create_event_locations()
    create_admin_message_settings()

    db.session.commit()


if __name__ == '__main__':
    with current_app.app_context():
        populate()
