"""empty message

Revision ID: 217c21289729
Revises: 784a1fc57171
Create Date: 2016-06-16 08:38:34.319436

"""

# revision identifiers, used by Alembic.
revision = '217c21289729'
down_revision = '784a1fc57171'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'sponsors_sponsor_type_id_fkey', 'sponsors', type_='foreignkey')
    op.drop_table('sponsor_type')
    op.add_column('sponsors', sa.Column('sponsor_type', sa.String(), nullable=True))
    # op.drop_constraint(u'sponsors_sponsor_type_id_fkey', 'sponsors', type_='foreignkey')
    op.drop_column('sponsors', 'sponsor_type_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'sponsors',
        sa.Column('sponsor_type_id', sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        u'sponsors_sponsor_type_id_fkey',
        'sponsors',
        'sponsor_type',
        ['sponsor_type_id'],
        ['id'],
        ondelete=u'CASCADE',
    )
    op.drop_column('sponsors', 'sponsor_type')
    op.create_table(
        'sponsor_type',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ['event_id'],
            [u'events.id'],
            name=u'sponsor_type_event_id_fkey',
            ondelete=u'CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=u'sponsor_type_pkey'),
    )
    ### end Alembic commands ###
