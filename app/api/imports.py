from flask import g
from flask import jsonify, url_for, current_app
from flask.ext.restplus import Resource, Namespace, marshal

from app.helpers.data import record_activity
from app.helpers.importers import ImportHelper
from events import EVENT
from helpers.helpers import requires_auth
from helpers.import_helpers import get_file_from_request, import_event_json, create_import_job, \
    send_import_mail
from helpers.utils import TASK_RESULTS

api = Namespace('imports', description='Imports', path='/')


@api.route('/events/import/json')
@api.hide
class EventImportJson(Resource):
    @requires_auth
    def post(self):
        file_path = get_file_from_request(['zip'])
        from helpers.tasks import import_event_task
        task = import_event_task.delay(file_path)
        # store import job in db
        try:
            create_import_job(task.id)
        except Exception:
            pass
        # if testing
        if current_app.config.get('CELERY_ALWAYS_EAGER'):
            send_import_mail(task.id, task.get())
            TASK_RESULTS[task.id] = {
                'result': task.get(),
                'state': task.state
            }
        return jsonify(
            task_url=url_for('api.extras_celery_task', task_id=task.id)
        )


@api.route('/events/import/pentabarf')
@api.hide
class EventImportPentabarf(Resource):
    @requires_auth
    def post(self):
        file_path = get_file_from_request(['xml'])
        from helpers.tasks import import_event_from_pentabarf_task
        task = import_event_from_pentabarf_task.delay(file_path, g.user)

        # store import job in db
        try:
            create_import_job(task.id)
        except Exception:
            pass
        # if testing
        if current_app.config.get('CELERY_ALWAYS_EAGER'):
            send_import_mail(task.id, task.get())
            TASK_RESULTS[task.id] = {
                'result': task.get(),
                'state': task.state
            }
        return jsonify(
            task_url=url_for('api.extras_celery_task', task_id=task.id)
        )


def import_event_task_base(task_handle, file_path, source_type='json', current_user=None):
    new_event = None
    if source_type == 'json':
        new_event = import_event_json(task_handle, file_path)
    elif source_type == 'pentabarf':
        new_event = ImportHelper.import_from_pentabarf(file_path=file_path, task_handle=task_handle,
                                                       creator=current_user)
    if new_event:
        record_activity('import_event', event_id=new_event.id)
        return marshal(new_event, EVENT)
    else:
        return None
