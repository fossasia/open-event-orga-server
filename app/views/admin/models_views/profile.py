from uuid import uuid4

from flask import request, url_for, redirect, abort, flash, jsonify
from flask.ext import login
from flask.ext.admin import BaseView
from flask_admin import expose
from markupsafe import Markup

from app.helpers.helpers import uploaded_file
from app.helpers.oauth import FbOAuth, InstagramOAuth
from app.helpers.storage import upload, UPLOAD_PATHS
from app.views.admin.models_views.events import is_verified_user
from ....helpers.data import DataManager, get_facebook_auth, get_instagram_auth, get_twitter_auth_url, save_to_db
from ....helpers.data_getter import DataGetter


class ProfileView(BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('admin.login_view', next=request.url))

    @expose('/')
    def index_view(self):
        if not is_verified_user():
            flash(Markup("Your account is unverified. "
                         "Please verify by clicking on the confirmation link that has been emailed to you."
                         '<br>Did not get the email? Please <a href="/resend_email/" class="alert-link"> '
                         'click here to resend the confirmation.</a>'))
        profile = DataGetter.get_user(login.current_user.id)
        return self.render('/gentelella/admin/profile/index.html',
                           profile=profile)

    @expose('/edit/', methods=('GET', 'POST'))
    @expose('/edit/<user_id>', methods=('GET', 'POST'))
    def edit_view(self, user_id=None):
        admin = None
        if not user_id:
            user_id = login.current_user.id
        else:
            admin = True
        if request.method == 'POST':
            url = ""
            DataManager.update_user(request.form, int(user_id), url)
            if admin:
                return redirect(url_for('sadmin_users.details_view', user_id=user_id))
            return redirect(url_for('.index_view'))
        profile = DataGetter.get_user(int(user_id))
        return self.render('/gentelella/admin/profile/edit.html', profile=profile)

    @expose('/fb_connect', methods=('GET', 'POST'))
    def connect_facebook(self):
        facebook = get_facebook_auth()
        fb_auth_url, state = facebook.authorization_url(FbOAuth.get_auth_uri(), access_type='offline')
        return redirect(fb_auth_url)

    @expose('/tw_connect', methods=('GET', 'POST'))
    def connect_twitter(self):
        twitter_auth_url, __ = get_twitter_auth_url()
        return redirect('https://api.twitter.com/oauth/authenticate?' + twitter_auth_url)

    @expose('/instagram_connect', methods=('GET', 'POST'))
    def connect_instagram(self):
        instagram = get_instagram_auth()
        instagram_auth_url, state = instagram.authorization_url(InstagramOAuth.get_auth_uri(), access_type='offline')
        return redirect(instagram_auth_url)

    @expose('/<int:user_id>/editfiles/bgimage', methods=('POST', 'DELETE'))
    def bgimage_upload(self, user_id):
        if request.method == 'POST':
            background_image = request.form['bgimage']
            if background_image:
                background_file = uploaded_file(file_content=background_image)
                background_url = upload(
                    background_file,
                    UPLOAD_PATHS['user']['avatar'].format(
                        user_id=user_id
                    ))
                return jsonify({'status': 'ok', 'background_url': background_url})
            else:
                return jsonify({'status': 'no bgimage'})
        elif request.method == 'DELETE':
            profile = DataGetter.get_user(int(user_id))
            profile.avatar_uploaded = ''
            save_to_db(profile)
            return jsonify({'status': 'ok'})

    @expose('/create/files/bgimage', methods=('POST',))
    def create_event_bgimage_upload(self):
        if request.method == 'POST':
            background_image = request.form['bgimage']
            if background_image:
                background_file = uploaded_file(file_content=background_image)
                background_url = upload(
                    background_file,
                    UPLOAD_PATHS['temp']['event'].format(uuid=uuid4())
                )
                return jsonify({'status': 'ok', 'background_url': background_url})
            else:
                return jsonify({'status': 'no bgimage'})


class NotificationView(BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('admin.login_view', next=request.url))

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        user = login.current_user
        notifications = DataGetter.get_all_user_notifications(user)

        return self.render('/gentelella/admin/profile/notifications.html',
                           notifications=notifications)

    @expose('/read/<notification_id>/', methods=('GET', 'POST'))
    def mark_as_read(self, notification_id):
        user = login.current_user
        notification = DataGetter.get_user_notification(notification_id)

        if notification and notification.user == user:
            DataManager.mark_user_notification_as_read(notification)
            return jsonify({'status': 'ok'})
        else:
            abort(404)

    @expose('/allread/', methods=('GET', 'POST'))
    def mark_all_read(self):
        user = login.current_user
        DataManager.mark_all_user_notification_as_read(user)

        return redirect(url_for('.index_view'))
