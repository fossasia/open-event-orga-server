"""empty message

Revision ID: aba0b1754103
Revises: ad789015cdf7
Create Date: 2017-07-10 23:50:18.373447

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'aba0b1754103'
down_revision = 'ad789015cdf7'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'access_codes_tickets',
        sa.Column('access_code_id', sa.Integer(), nullable=False),
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['access_code_id'], ['access_codes.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('access_code_id', 'ticket_id'),
    )
    op.drop_column(u'access_codes', 'tickets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        u'access_codes',
        sa.Column('tickets', sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_table('access_codes_tickets')
    # ### end Alembic commands ###
