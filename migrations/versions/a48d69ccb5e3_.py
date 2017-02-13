"""empty message

Revision ID: a48d69ccb5e3
Revises: c4b4889d5e4e
Create Date: 2017-02-12 15:55:10.922212

"""

# revision identifiers, used by Alembic.
revision = 'a48d69ccb5e3'
down_revision = 'c4b4889d5e4e'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'orders_tickets_ticket_id_fkey', 'orders_tickets', type_='foreignkey')
    op.drop_column('orders_tickets', 'ticket_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders_tickets', sa.Column('ticket_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key(u'orders_tickets_ticket_id_fkey', 'orders_tickets', 'ticket', ['ticket_id'], ['id'], ondelete=u'CASCADE')
    # ### end Alembic commands ###
