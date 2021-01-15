"""empty message

Revision ID: a742abacc9b6
Revises: a3fb59fea6c2
Create Date: 2021-01-15 13:41:59.392788

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'a742abacc9b6'
down_revision = 'a3fb59fea6c2'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_favourite_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_id', 'user_id', name='uq_session_user')
    )
    op.add_column('events', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'events', 'groups', ['group_id'], ['id'], ondelete='SET NULL')
    op.add_column('events_version', sa.Column('group_id', sa.Integer(), autoincrement=False, nullable=True))
    op.alter_column('users', 'is_blocked',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_blocked',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.drop_column('events_version', 'group_id')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'group_id')
    op.drop_table('user_favourite_sessions')
    op.drop_table('groups')
    # ### end Alembic commands ###
