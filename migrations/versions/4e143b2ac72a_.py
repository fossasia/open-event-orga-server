"""empty message

Revision ID: 4e143b2ac72a
Revises: 8cdaeb567de4
Create Date: 2016-07-23 09:02:51.743000

"""

# revision identifiers, used by Alembic.
revision = '4e143b2ac72a'
down_revision = '8cdaeb567de4'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticket_include', sa.Boolean(), nullable=True),
        sa.Column('payment_include', sa.Boolean(), nullable=True),
        sa.Column('donation_include', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.add_column(u'events', sa.Column('ticket_include', sa.Boolean(), nullable=True))
    op.add_column(
        u'events_version',
        sa.Column('ticket_include', sa.Boolean(), autoincrement=False, nullable=True),
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'events_version', 'ticket_include')
    op.drop_column(u'events', 'ticket_include')
    op.drop_table('modules')
    ### end Alembic commands ###
