from app.api.helpers.utilities import dasherize
from app.models.activity import Activity
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class ActivitySchema(SQLAlchemyAutoSchema):
    """
    Api schema for Activity Model
    """
    class Meta:
        """
        Meta class for Activity Api Schema
        """
        type_ = 'activity'
        self_view = 'v1.activity_detail'
        self_view_kwargs = {'id': '<id>'}
        inflect = dasherize

        model = Activity
        dump_only = ("id",)
        load_instance = True
        include_fk = True
