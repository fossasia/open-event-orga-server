"""empty message

Revision ID: 49994f8ad895
Revises: c32364a17072
Create Date: 2021-03-26 02:13:43.472556

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '49994f8ad895'
down_revision = 'c32364a17072'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('chat_room_id', sa.String(), nullable=True))
    op.add_column('events_version', sa.Column('chat_room_id', sa.String(), autoincrement=False, nullable=True))
    op.add_column('settings', sa.Column('rocket_bot_email', sa.String(), nullable=True))
    op.add_column('settings', sa.Column('rocket_bot_name', sa.String(), nullable=True))
    op.add_column('settings', sa.Column('rocket_bot_password', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events_version', 'chat_room_id')
    op.drop_column('events', 'chat_room_id')
    op.drop_column('settings', 'rocket_bot_password')
    op.drop_column('settings', 'rocket_bot_name')
    op.drop_column('settings', 'rocket_bot_email')
    # ### end Alembic commands ###
