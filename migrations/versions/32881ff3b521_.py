"""empty message

Revision ID: 32881ff3b521
Revises: b4fdb245fccd
Create Date: 2017-08-24 16:32:45.481306

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32881ff3b521'
down_revision = 'b4fdb245fccd'


def upgrade():
    # commands auto generated by Alembic - please adjust! #
    op.create_table(
        'faq',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(), nullable=False),
        sa.Column('answer', sa.String(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # commands auto generated by Alembic - please adjust! #
    op.drop_table('faq')
    # ### end Alembic commands ###
