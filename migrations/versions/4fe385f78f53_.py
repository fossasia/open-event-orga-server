"""empty message

Revision ID: 4fe385f78f53
Revises: 2b1ace2d613d
Create Date: 2018-07-23 10:35:57.960005

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '4fe385f78f53'
down_revision = '2b1ace2d613d'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_marketer', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_sales_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_sales_admin')
    op.drop_column('users', 'is_marketer')
    # ### end Alembic commands ###
