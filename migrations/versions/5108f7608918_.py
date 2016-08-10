"""empty message

Revision ID: 5108f7608918
Revises: 92d65554495c
Create Date: 2016-08-07 13:12:08.835000

"""

# revision identifiers, used by Alembic.
revision = '5108f7608918'
down_revision = '92d65554495c'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'token', new_column_name='stripe_token')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'stripe_token', new_column_name='token')
    ### end Alembic commands ###
