"""empty message

Revision ID: 81ac738516a0
Revises: 35a4c25f12e5
Create Date: 2018-07-30 12:57:09.572293

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '81ac738516a0'
down_revision = '35a4c25f12e5'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    events_table = sa.sql.table('events', sa.Column('order_expiry_time', sa.Integer))
    op.execute(
        events_table.update()
        .where(events_table.c.order_expiry_time.is_(None))
        .values({'order_expiry_time': 10})
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    pass
