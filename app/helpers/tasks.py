import requests
import os
import errno
from flask import current_app as app
from marrow.mailer import Mailer, Message
from app import celery
from app.helpers.versioning import strip_tags
from app.helpers.exporters.pentabarfxml import PentabarfExporter
from app.helpers.exporters.ical import ICalExporter
from app.helpers.exporters.xcal import XCalExporter
from app.helpers.storage import UPLOAD_PATHS, upload, UploadedFile
from app.helpers.data_getter import DataGetter
from app.helpers.data import save_to_db


@celery.task(name='send.email.post')
def send_email_task(payload, headers):
    requests.post(
        "https://api.sendgrid.com/api/mail.send.json",
        data=payload,
        headers=headers
    )


@celery.task(name='send.email.post.smtp')
def send_mail_via_smtp_task(config, payload):
    mailer_config = {
        'transport': {
            'use': 'smtp',
            'host': config['host'],
            'username': config['username'],
            'password': config['password'],
            'tls': config['encryption'],
            'port': config['port']
        }
    }

    mailer = Mailer(mailer_config)
    mailer.start()
    message = Message(author=payload['from'], to=payload['to'])
    message.subject = payload['subject']
    message.plain = strip_tags(payload['html'])
    message.rich = payload['html']
    mailer.send(message)
    mailer.stop()


@celery.task(name='export.pentabarf')
def export_pentabarf_task(event_id):
    event = DataGetter.get_event(event_id)
    try:
        os.mkdir(app.config['TEMP_UPLOADS_FOLDER'])
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
    filename = "pentabarf.xml"
    file_path = app.config['TEMP_UPLOADS_FOLDER'] + "/" + filename
    with open(file_path, "w") as temp_file:
        temp_file.write(PentabarfExporter.export(event_id))
    pentabarf_file = UploadedFile(file_path=file_path, filename=filename)
    event.pentabarf_url = upload(pentabarf_file, UPLOAD_PATHS['exports']['pentabarf'].format(event_id=event_id))
    save_to_db(event)


@celery.task(name='export.ical')
def export_ical_task(event_id):
    event = DataGetter.get_event(event_id)
    try:
        os.mkdir(app.config['TEMP_UPLOADS_FOLDER'])
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
    filename = "ical.ics"
    file_path = app.config['TEMP_UPLOADS_FOLDER'] + "/" + filename
    with open(file_path, "w") as temp_file:
        temp_file.write(ICalExporter.export(event_id))
    ical_file = UploadedFile(file_path=file_path, filename=filename)
    event.ical_url = upload(ical_file, UPLOAD_PATHS['exports']['ical'].format(event_id=event_id))
    save_to_db(event)


@celery.task(name='export.xcal')
def export_xcal_task(event_id):
    event = DataGetter.get_event(event_id)
    try:
        os.mkdir(app.config['TEMP_UPLOADS_FOLDER'])
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
    filename = "xcal.xcs"
    file_path = app.config['TEMP_UPLOADS_FOLDER'] + "/" + filename
    with open(file_path, "w") as temp_file:
        temp_file.write(XCalExporter.export(event_id))
    xcal_file = UploadedFile(file_path=file_path, filename=filename)
    event.xcal_url = upload(xcal_file, UPLOAD_PATHS['exports']['xcal'].format(event_id=event_id))
    save_to_db(event)
