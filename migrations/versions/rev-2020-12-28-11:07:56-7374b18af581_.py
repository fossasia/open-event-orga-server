"""empty message

Revision ID: 7374b18af581
Revises: b0c55c767022
Create Date: 2020-12-28 11:07:56.703331

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '7374b18af581'
down_revision = 'b0c55c767022'


def upgrade():
    op.execute("UPDATE custom_forms SET is_public=True WHERE form='session' and (field_identifier='title' or field_identifier='short_abstract' or field_identifier='track' or field_identifier='session_type' or field_identifier='language' or field_identifier='slides' or field_identifier='video');")
    op.execute("UPDATE custom_forms SET is_public=True WHERE form='speaker' and (field_identifier='name' or field_identifier='photo' or field_identifier='country' or field_identifier='short_biography' or field_identifier='website' or field_identifier='facebook' or field_identifier='github' or field_identifier='twitter' or field_identifier='linkedin');")

def downgrade():
	op.execute("UPDATE custom_forms SET is_public=False WHERE form='session' and (field_identifier='title' or field_identifier='short_abstract' or field_identifier='track' or field_identifier='session_type' or field_identifier='language' or field_identifier='slides' or field_identifier='video');")
    op.execute("UPDATE custom_forms SET is_public=False WHERE form='speaker' and (field_identifier='name' or field_identifier='photo' or field_identifier='country' or field_identifier='short_biography' or field_identifier='website' or field_identifier='facebook' or field_identifier='github' or field_identifier='twitter' or field_identifier='linkedin');")