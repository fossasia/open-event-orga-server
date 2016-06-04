from flask import request, url_for, redirect
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask.ext import login
from ....helpers.data import DataManager
from ....helpers.data_getter import DataGetter


class ProfileView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('admin.login_view', next=request.url))

    @expose('/')
    def index_view(self):
        profile = DataGetter.get_user(login.current_user.id)
        return self.render('/gentelella/admin/profile/index.html',
                           profile=profile)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        if request.method == 'POST':
            profile = DataManager.update_user(request.form, login.current_user.id)
            return redirect(url_for('.index_view'))
        profile = DataGetter.get_user(login.current_user.id)
        return self.render('/gentelella/admin/profile/edit.html', profile=profile)
