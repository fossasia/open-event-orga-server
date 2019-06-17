"""empty message

Revision ID: 76aed36b4888
Revises: 6f7b6fad3f56
Create Date: 2019-05-30 18:45:32.787787

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '76aed36b4888'
down_revision = '6f7b6fad3f56'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('can_pay_by_alipay', sa.Boolean(), nullable=True))
    op.add_column('events_version', sa.Column('can_pay_by_alipay', sa.Boolean(), autoincrement=False, nullable=True))
    op.add_column('settings', sa.Column('alipay_publishable_key', sa.String(), nullable=True))
    op.add_column('settings', sa.Column('alipay_secret_key', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events_version', 'can_pay_by_alipay')
    op.drop_column('events', 'can_pay_by_alipay')
    op.drop_column('settings', 'alipay_secret_key')
    op.drop_column('settings', 'alipay_publishable_key')
    # ### end Alembic commands ###
