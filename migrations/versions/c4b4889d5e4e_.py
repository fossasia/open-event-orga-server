"""empty message

Revision ID: c4b4889d5e4e
Revises: d73fc7833958
Create Date: 2017-01-30 18:04:36.323708

"""

# revision identifiers, used by Alembic.
revision = 'c4b4889d5e4e'
down_revision = 'd73fc7833958'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('speaker', 'country',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('speaker', 'organisation',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('speaker', 'organisation',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('speaker', 'country',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
