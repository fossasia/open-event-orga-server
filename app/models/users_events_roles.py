from . import db


class UsersEventsRoles(db.Model):
    __tablename__ = 'users_events_roles'

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship("Role")

    def __init__(self, user, event, role):
        self.user = user
        self.event = event
        self.role = role

    def __repr__(self):
        return '<UER %r:%r:%r>' % (self.user,
                                   self.event_id,
                                   self.role, )

    def __str__(self):
        return str(self).encode('utf-8')

    def __unicode__(self):
        return '%r: %r in %r' % (self.user,
                                 self.role,
                                 self.event_id, )
