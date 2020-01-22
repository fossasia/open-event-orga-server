"""empty message

Revision ID: 10841bb4b0ea
Revises: 91f664d0007e
Create Date: 2018-07-26 07:30:02.870141

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10841bb4b0ea'
down_revision = '91f664d0007e'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('order_expiry_time', sa.Integer(), nullable=True))
    op.add_column(
        'events_version',
        sa.Column(
            'order_expiry_time', sa.Integer(), autoincrement=False, nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events_version', 'order_expiry_time')
    op.drop_column('events', 'order_expiry_time')
    # ### end Alembic commands ###
