"""empty message

Revision ID: fd3b97c8cc9a
Revises: 3a9c159811ae
Create Date: 2016-08-05 22:38:02.060000

"""

# revision identifiers, used by Alembic.
revision = 'fd3b97c8cc9a'
down_revision = '3a9c159811ae'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('discount_codes', 'tickets_number')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'discount_codes',
        sa.Column('tickets_number', sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    ### end Alembic commands ###
