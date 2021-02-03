"""empty message

Revision ID: 455aaf926647
Revises: b75a8dd29262
Create Date: 2021-02-03 09:50:17.628577

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '455aaf926647'
down_revision = 'b75a8dd29262'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video_stream_moderator',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video_stream_moderator')
    # ### end Alembic commands ###
