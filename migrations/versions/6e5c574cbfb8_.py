"""empty message

Revision ID: 6e5c574cbfb8
Revises: 35f427e85075
Create Date: 2019-03-24 11:09:42.707206

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e5c574cbfb8'
down_revision = '35f427e85075'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE orders SET amount = 0 WHERE amount = NULL", execution_options=None)
    op.alter_column('orders', 'amount',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False,
               )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'amount',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    # ### end Alembic commands ###
