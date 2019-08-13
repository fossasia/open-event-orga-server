"""empty message

Revision ID: cd3beca1951a
Revises: 1bdf23be63bd
Create Date: 2019-08-13 16:07:52.020447

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'cd3beca1951a'
down_revision = '1bdf23be63bd'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('settings', sa.Column('stripe_test_client_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'stripe_test_client_id')
    # ### end Alembic commands ###
