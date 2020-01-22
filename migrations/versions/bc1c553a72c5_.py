"""empty message

Revision ID: bc1c553a72c5
Revises: 740b89e12cbb
Create Date: 2017-07-08 16:11:34.326573

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'bc1c553a72c5'
down_revision = '740b89e12cbb'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('speaker', sa.Column('is_featured', sa.Boolean(), nullable=True))
    op.drop_column('speaker', 'featured')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'speaker',
        sa.Column('featured', sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.drop_column('speaker', 'is_featured')
    # ### end Alembic commands ###
