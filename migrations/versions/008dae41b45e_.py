"""empty message

Revision ID: 008dae41b45e
Revises: 0d25e6904746
Create Date: 2016-06-09 04:53:33.428575

"""

# revision identifiers, used by Alembic.
revision = '008dae41b45e'
down_revision = '0d25e6904746'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'nickname')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'user',
        sa.Column(
            'nickname', sa.VARCHAR(length=100), autoincrement=False, nullable=True
        ),
    )
    ### end Alembic commands ###
