from flask.ext.admin import BaseView
from flask_admin import expose
from ....helpers.data_getter import DataGetter
from open_event.helpers.permission_decorators import *

class SponsorsView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index_view(self, event_id):
        sponsors = DataGetter.get_sponsors(event_id)
        event = DataGetter.get_event(event_id)
        return self.render('/gentelella/admin/event/sponsors/display.html',
                           sponsors=sponsors, event_id=event_id, event=event)

    @expose('/new/', methods=('GET', 'POST'))
    @can_access
    def create_view(self, event_id):
        event = DataGetter.get_event(event_id)
        return self.render('/gentelella/admin/event/sponsors/new.html', event_id=event_id, event=event)

    @expose('/<speaker_id>/delete/', methods=('POST',))
    @can_access
    def delete_view(self, event_id,sponsor_id):
        return ''

    @expose('/<speaker_id>/edit/', methods=('POST', 'GET'))
    @can_access
    def edit_view(self, event_id, sponsor_id):
        event = DataGetter.get_event(event_id)
        return self.render('/gentelella/admin/event/sponsors/edit.html', event_id=event_id, event=event)
