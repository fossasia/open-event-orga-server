"""empty message

Revision ID: 047f7c3db184
Revises: dd24d9e90809
Create Date: 2016-07-12 11:28:08.051094

"""

# revision identifiers, used by Alembic.
revision = '047f7c3db184'
down_revision = 'dd24d9e90809'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'pages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('place', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pages')
    ### end Alembic commands ###
