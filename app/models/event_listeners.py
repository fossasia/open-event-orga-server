from sqlalchemy.event import listens_for

from .event import Event
from .version import Version


@listens_for(Event, "after_insert")
def after_insert(mapper, connection, target):
    """Update Version after insert to db"""
    link_table = Version.__table__
    version = Version.query.order_by(Version.id.desc()).first()
    if version:
        version_id = version.id
        connection.execute(link_table.update().where(
            link_table.c.id == version_id).values(event_id=target.id))
