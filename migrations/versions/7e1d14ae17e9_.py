"""empty message

Revision ID: 7e1d14ae17e9
Revises: e85aaacd8721
Create Date: 2017-07-12 15:41:44.230025

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '7e1d14ae17e9'
down_revision = 'e85aaacd8721'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'custom_placeholders',
        sa.Column('event_sub_topic_id', sa.Integer(), nullable=True),
    )
    op.add_column(
        'custom_placeholders', sa.Column('icon_image_url', sa.String(), nullable=True)
    )
    op.add_column(
        'custom_placeholders', sa.Column('large_image_url', sa.String(), nullable=True)
    )
    op.alter_column(
        'custom_placeholders',
        'url',
        new_column_name='original_image_url',
        nullable=False,
    )
    op.alter_column(
        'custom_placeholders',
        'thumbnail',
        new_column_name='thumbnail_image_url',
        nullable=True,
    )
    op.execute(
        "UPDATE custom_placeholders SET icon_image_url = original_image_url, large_image_url=original_image_url"
    )
    op.execute(
        "UPDATE custom_placeholders SET thumbnail_image_url = original_image_url WHERE thumbnail_image_url is NULL or thumbnail_image_url=''"
    )
    op.alter_column('custom_placeholders', 'icon_image_url', nullable=False)
    op.alter_column('custom_placeholders', 'large_image_url', nullable=False)
    op.alter_column('custom_placeholders', 'thumbnail_image_url', nullable=False)
    op.create_foreign_key(
        'custom_placeholders_event_sub_topics',
        'custom_placeholders',
        'event_sub_topics',
        ['event_sub_topic_id'],
        ['id'],
        ondelete='CASCADE',
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'custom_placeholders',
        'original_image_url',
        new_column_name='url',
        nullable=True,
    )
    op.alter_column(
        'custom_placeholders',
        'thumbnail_image_url',
        new_column_name='thumbnail',
        nullable=True,
    )
    op.drop_constraint(
        'custom_placeholders_event_sub_topics',
        'custom_placeholders',
        type_='foreignkey',
    )
    op.drop_column('custom_placeholders', 'large_image_url')
    op.drop_column('custom_placeholders', 'icon_image_url')
    op.drop_column('custom_placeholders', 'event_sub_topic_id')
    # ### end Alembic commands ###
