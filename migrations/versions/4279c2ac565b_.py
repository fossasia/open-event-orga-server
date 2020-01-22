"""empty message

Revision ID: 4279c2ac565b
Revises: 2c7ff9781032
Create Date: 2019-06-28 09:37:30.961354

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '4279c2ac565b'
down_revision = '2c7ff9781032'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users', sa.Column('billing_additional_info', sa.String(), nullable=True)
    )
    op.add_column('users', sa.Column('billing_address', sa.String(), nullable=True))
    op.add_column('users', sa.Column('billing_city', sa.String(), nullable=True))
    op.add_column(
        'users', sa.Column('billing_contact_name', sa.String(), nullable=True)
    )
    op.add_column('users', sa.Column('billing_country', sa.String(), nullable=True))
    op.add_column('users', sa.Column('billing_phone', sa.String(), nullable=True))
    op.add_column('users', sa.Column('billing_tax_info', sa.String(), nullable=True))
    op.add_column('users', sa.Column('billing_zip_code', sa.String(), nullable=True))
    op.add_column('users', sa.Column('company', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'company')
    op.drop_column('users', 'billing_zip_code')
    op.drop_column('users', 'billing_tax_info')
    op.drop_column('users', 'billing_phone')
    op.drop_column('users', 'billing_country')
    op.drop_column('users', 'billing_contact_name')
    op.drop_column('users', 'billing_city')
    op.drop_column('users', 'billing_address')
    op.drop_column('users', 'billing_additional_info')
    # ### end Alembic commands ###
