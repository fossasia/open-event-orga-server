"""empty message

Revision ID: dd7968d8d413
Revises: 49f3a33f5437
Create Date: 2018-06-02 21:57:00.799206

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dd7968d8d413'
down_revision = '49f3a33f5437'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'image_sizes', sa.Column('icon_size_quality', sa.Integer(), nullable=True)
    )
    op.add_column(
        'image_sizes', sa.Column('icon_size_width_height', sa.Integer(), nullable=True)
    )
    op.add_column(
        'image_sizes', sa.Column('small_size_quality', sa.Integer(), nullable=True)
    )
    op.add_column(
        'image_sizes', sa.Column('small_size_width_height', sa.Integer(), nullable=True)
    )
    op.add_column(
        'image_sizes', sa.Column('thumbnail_size_quality', sa.Integer(), nullable=True)
    )
    op.add_column(
        'image_sizes',
        sa.Column('thumbnail_size_width_height', sa.Integer(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('image_sizes', 'thumbnail_size_width_height')
    op.drop_column('image_sizes', 'thumbnail_size_quality')
    op.drop_column('image_sizes', 'small_size_width_height')
    op.drop_column('image_sizes', 'small_size_quality')
    op.drop_column('image_sizes', 'icon_size_width_height')
    op.drop_column('image_sizes', 'icon_size_quality')
    # ### end Alembic commands ###
