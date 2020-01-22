"""add stripe test keys

Revision ID: f5c3a4fd23fb
Revises: 4925dd5fd720
Create Date: 2019-08-07 01:11:29.736517

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'f5c3a4fd23fb'
down_revision = '4925dd5fd720'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'settings', sa.Column('stripe_test_publishable_key', sa.String(), nullable=True)
    )
    op.add_column(
        'settings', sa.Column('stripe_test_secret_key', sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'stripe_test_secret_key')
    op.drop_column('settings', 'stripe_test_publishable_key')
    # ### end Alembic commands ###
