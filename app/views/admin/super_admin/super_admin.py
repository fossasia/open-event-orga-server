import os

from flask_admin import expose

from app.views.admin.super_admin.super_admin_base import SuperAdminBaseView
from ....helpers.data_getter import DataGetter
from app.helpers.helpers import get_latest_heroku_release, get_commit_info, get_count
from app.models.user import ATTENDEE,TRACK_ORGANIZER, COORGANIZER, ORGANIZER
from app.helpers.kubernetes import KubernetesApi


class SuperAdminView(SuperAdminBaseView):

    @expose('/')
    def index_view(self):
        events = DataGetter.get_all_events()[:5]
        number_live_events = get_count(DataGetter.get_all_live_events())
        number_draft_events = get_count(DataGetter.get_all_draft_events())
        number_past_events = get_count(DataGetter.get_all_past_events())
        super_admins = DataGetter.get_all_super_admins()
        admins = DataGetter.get_all_admins()
        registered_users = DataGetter.get_all_registered_users()
        # TODO Fix function and correct this
        organizers = get_count(DataGetter.get_all_user_roles(ORGANIZER))
        co_organizers = get_count(DataGetter.get_all_user_roles(COORGANIZER))
        track_organizers = get_count(DataGetter.get_all_user_roles(TRACK_ORGANIZER))
        attendees = get_count(DataGetter.get_all_user_roles(ATTENDEE))
        accepted_sessions = DataGetter.get_all_accepted_sessions()
        rejected_sessions = DataGetter.get_all_rejected_sessions()
        draft_sessions = DataGetter.get_all_draft_sessions()
        email_times = DataGetter.get_email_by_times()

        commit_info = None
        version = None
        on_kubernetes = False
        pods_info = None

        if KubernetesApi.is_on_kubernetes():
            on_kubernetes = True
            kubernetes_api = KubernetesApi()
            pods_info = kubernetes_api.get_pods()['items']
            version = os.getenv('REPOSITORY', 'https://github.com/fossasia/open-event-orga-server.git')
            commit_info = os.getenv('BRANCH', 'development')
        else:
            version = get_latest_heroku_release()
            commit_info = None
            commit_number = None
            if version:
                commit_number = version['description'].split(' ')[1]
                commit_info = get_commit_info(commit_number)

        return self.render('/gentelella/admin/super_admin/widgets/index.html',
                           events=events,
                           version=version,
                           commit_info=commit_info,
                           on_kubernetes=on_kubernetes,
                           pods_info=pods_info,
                           number_live_events=number_live_events,
                           number_draft_events=number_draft_events,
                           number_past_events=number_past_events,
                           super_admins=super_admins,
                           admins=admins,
                           registered_users=registered_users,
                           organizers=organizers,
                           co_organizers=co_organizers,
                           track_organizers=track_organizers,
                           attendees=attendees,
                           accepted_sessions=accepted_sessions,
                           rejected_sessions=rejected_sessions,
                           draft_sessions=draft_sessions,
                           email_times=email_times)
