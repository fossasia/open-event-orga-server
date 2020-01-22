"""empty message

Revision ID: ae95fb82282d
Revises: ebf41490ac7d
Create Date: 2018-06-23 20:01:44.723289

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae95fb82282d'
down_revision = 'ebf41490ac7d'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'speakers_calls',
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        'tax', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        'event_copyrights',
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('speakers_calls', 'deleted_at')
    op.drop_column('tax', 'deleted_at')
    op.drop_column('event_copyrights', 'deleted_at')
    # ### end Alembic commands ###
