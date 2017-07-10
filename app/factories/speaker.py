import factory
from app.models.speaker import db, Speaker
from app.factories.event import EventFactoryBasic
import app.factories.common as common


class SpeakerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Speaker
        sqlalchemy_session = db.session

    event = factory.RelatedFactory(EventFactoryBasic)
    name = common.string_
    email = common.email_
    photo_url = common.url_
    thumbnail_image_url = common.url_
    small_image_url = common.url_
    icon_image_url = common.url_
    short_biography = common.string_
    long_biography = common.string_
    speaking_experience = common.string_
    mobile = common.string_
    website = common.url_
    twitter = common.url_
    facebook = common.url_
    github = common.url_
    linkedin = common.url_
    organisation = common.string_
    is_featured = False
    position = common.string_
    country = common.string_
    city = common.string_
    gender = common.string_
    heard_from = common.string_
    sponsorship_required = common.string_
