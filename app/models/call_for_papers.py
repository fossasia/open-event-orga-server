from sqlalchemy.orm import backref

from . import db


class CallForPaper(db.Model):
    """call for paper model class"""
    __tablename__ = 'call_for_papers'
    id = db.Column(db.Integer, primary_key=True)
    announcement = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    timezone = db.Column(db.String, nullable=False, default="UTC")
    hash = db.Column(db.String, nullable=True)
    privacy = db.Column(db.String, nullable=False)
    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    events = db.relationship("Event", backref=backref("call_for_papers", uselist=False))

    def __init__(self, announcement=None, start_date=None, end_date=None, timezone='UTC', hash=None, privacy='public', event_id=None):
        self.announcement = announcement
        self.start_date = start_date
        self.end_date = end_date
        self.timezone = timezone
        self.hash = hash
        self.privacy = privacy
        self.event_id = event_id

    def __repr__(self):
        return '<call_for_papers %r>' % self.announcement

    def __str__(self):
        return str(self).encode('utf-8')

    def __unicode__(self):
        return self.announcement

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        return {'id': self.id,
                'announcement': self.announcement,
                'start_date':self.start_date,
                'end_date':self.end_date,
                'timezone':self.timezone}
