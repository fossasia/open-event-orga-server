"""empty message

Revision ID: a0532f339abb
Revises: e59e7a75f679
Create Date: 2019-05-05 02:29:08.380691

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0532f339abb'
down_revision = 'e59e7a75f679'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'settings', sa.Column('omise_live_public', sa.String(), nullable=True)
    )
    op.add_column(
        'settings', sa.Column('omise_live_secret', sa.String(), nullable=True)
    )
    op.add_column('settings', sa.Column('omise_mode', sa.String(), nullable=True))
    op.add_column(
        'settings', sa.Column('omise_test_public', sa.String(), nullable=True)
    )
    op.add_column(
        'settings', sa.Column('omise_test_secret', sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'omise_test_secret')
    op.drop_column('settings', 'omise_test_public')
    op.drop_column('settings', 'omise_mode')
    op.drop_column('settings', 'omise_live_secret')
    op.drop_column('settings', 'omise_live_public')
    # ### end Alembic commands ###
