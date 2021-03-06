"""add column is_email_overriden to speaker table

Revision ID: 96bca587b3ca
Revises: facee76912bc
Create Date: 2019-07-18 04:50:05.175917

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '96bca587b3ca'
down_revision = 'facee76912bc'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('speaker', sa.Column('is_email_overridden', sa.Boolean(), server_default='False', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('speaker', 'is_email_overridden')
    # ### end Alembic commands ###
