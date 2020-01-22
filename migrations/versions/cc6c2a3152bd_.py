"""empty message

Revision ID: cc6c2a3152bd
Revises: 752be2444e8d
Create Date: 2016-07-29 20:18:15.871000

"""

# revision identifiers, used by Alembic.
revision = 'cc6c2a3152bd'
down_revision = '752be2444e8d'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'settings', sa.Column('stripe_publishable_key', sa.String(), nullable=True)
    )
    op.add_column(
        'settings', sa.Column('stripe_secret_key', sa.String(), nullable=True)
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'stripe_secret_key')
    op.drop_column('settings', 'stripe_publishable_key')
    ### end Alembic commands ###
