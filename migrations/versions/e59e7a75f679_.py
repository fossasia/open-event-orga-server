"""empty message

Revision ID: e59e7a75f679
Revises: 5551af72812f
Create Date: 2019-04-19 13:27:05.212985

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'e59e7a75f679'
down_revision = '5551af72812f'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'events',
        sa.Column('is_featured', sa.Boolean(), server_default='False', nullable=False),
    )
    op.add_column(
        'events_version',
        sa.Column(
            'is_featured',
            sa.Boolean(),
            server_default='False',
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events_version', 'is_featured')
    op.drop_column('events', 'is_featured')
    # ### end Alembic commands ###
