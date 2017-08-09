"""empty message

Revision ID: bf3e8c2a01f6
Revises: dbb9670cd902
Create Date: 2017-08-08 17:09:52.402284

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'bf3e8c2a01f6'
down_revision = 'dbb9670cd902'


def upgrade():
    # commands auto generated by Alembic - please adjust! #
    op.create_table('export_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(), nullable=False),
    sa.Column('starts_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_email', sa.String(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stripe_authorizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stripe_secret_key', sa.String(), nullable=True),
    sa.Column('stripe_refresh_token', sa.String(), nullable=True),
    sa.Column('stripe_publishable_key', sa.String(), nullable=True),
    sa.Column('stripe_user_id', sa.String(), nullable=True),
    sa.Column('stripe_email', sa.String(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # end Alembic commands #


def downgrade():
    # commands auto generated by Alembic - please adjust! #
    op.drop_table('stripe_authorizations')
    op.drop_table('export_jobs')
    # end Alembic commands #
