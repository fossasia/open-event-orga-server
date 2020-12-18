"""empty message

Revision ID: 286869159bb5
Revises: 8aef207c014f
Create Date: 2020-07-24 21:26:41.814719

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '286869159bb5'
down_revision = '8aef207c014f'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('modules')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('modules',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ticket_include', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('payment_include', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('donation_include', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='modules_pkey')
    )
    # ### end Alembic commands ###
