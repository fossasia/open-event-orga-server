"""empty message

Revision ID: 1bdf23be63bd
Revises: 246b5b6123af
Create Date: 2019-08-13 14:38:26.081952

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '9172ceb350b8'
down_revision = '90d62fe3b5e3'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_ticket_tag', 'ticket_tag', ['name', 'event_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_ticket_tag', 'ticket_tag', type_='unique')
    # ### end Alembic commands ###
