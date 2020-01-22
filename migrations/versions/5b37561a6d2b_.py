"""empty message

Revision ID: 5b37561a6d2b
Revises: 27c4db7538ca
Create Date: 2016-06-26 21:37:39.740000

"""

# revision identifiers, used by Alembic.
revision = '5b37561a6d2b'
down_revision = '27c4db7538ca'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('code_of_conduct', sa.String(), nullable=True))
    op.add_column(
        'events_version',
        sa.Column('code_of_conduct', sa.String(), autoincrement=False, nullable=True),
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events_version', 'code_of_conduct')
    op.drop_column('events', 'code_of_conduct')
    ### end Alembic commands ###
