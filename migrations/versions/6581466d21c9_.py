"""empty message

Revision ID: 6581466d21c9
Revises: 11143ed3e6fa
Create Date: 2017-01-02 18:53:59.592709

"""

# revision identifiers, used by Alembic.
revision = '6581466d21c9'
down_revision = '11143ed3e6fa'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session', sa.Column('level', sa.String(), nullable=True))
    op.add_column(
        'session_version',
        sa.Column('level', sa.String(), autoincrement=False, nullable=True),
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('session_version', 'level')
    op.drop_column('session', 'level')
    ### end Alembic commands ###
