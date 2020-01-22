"""empty message

Revision ID: 740b89e12cbb
Revises: 63deafdfebd6
Create Date: 2017-07-05 18:33:54.710619

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '740b89e12cbb'
down_revision = '63deafdfebd6'


def upgrade():
    # commands auto generated by Alembic - please adjust! #
    op.execute(
        "DELETE FROM event_copyrights WHERE licence='' or licence IS NULL ",
        execution_options=None,
    )
    op.execute(
        "DELETE FROM sessions WHERE title='' or title IS NULL", execution_options=None
    )
    op.execute(
        "DELETE FROM social_links WHERE link='' or link IS NULL", execution_options=None
    )
    op.execute(
        "DELETE FROM speakers_calls WHERE announcement='' or announcement IS NULL",
        execution_options=None,
    )
    op.execute(
        "DELETE FROM ticket_holders WHERE firstname='' or firstname IS NULL",
        execution_options=None,
    )
    op.execute(
        "DELETE FROM tickets WHERE name='' or name IS NULL", execution_options=None
    )
    op.execute(
        "DELETE FROM tickets WHERE sales_ends_at IS NULL", execution_options=None
    )
    op.execute(
        "DELETE FROM tickets WHERE sales_starts_at IS NULL", execution_options=None
    )
    op.execute(
        "DELETE FROM tickets WHERE type='' or type IS NULL", execution_options=None
    )
    op.execute(
        "DELETE FROM users WHERE _email='' or _email IS NULL", execution_options=None
    )
    op.execute(
        "DELETE FROM users WHERE _password='' or _password IS NULL",
        execution_options=None,
    )
    op.alter_column(
        'event_copyrights', 'licence', existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column('sessions', 'title', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('social_links', 'link', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        'speakers_calls', 'announcement', existing_type=sa.TEXT(), nullable=False
    )
    op.alter_column(
        'ticket_holders', 'firstname', existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column('tickets', 'name', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        'tickets',
        'sales_ends_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    op.alter_column(
        'tickets',
        'sales_starts_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    op.alter_column('tickets', 'type', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        'users', '_email', existing_type=sa.VARCHAR(length=120), nullable=False
    )
    op.alter_column(
        'users', '_password', existing_type=sa.VARCHAR(length=128), nullable=False
    )
    # end Alembic commands #


def downgrade():
    # commands auto generated by Alembic - please adjust! #
    op.alter_column(
        'users', '_password', existing_type=sa.VARCHAR(length=128), nullable=True
    )
    op.alter_column(
        'users', '_email', existing_type=sa.VARCHAR(length=120), nullable=True
    )
    op.alter_column('tickets', 'type', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        'tickets',
        'sales_starts_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
    op.alter_column(
        'tickets',
        'sales_ends_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
    op.alter_column('tickets', 'name', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        'ticket_holders', 'firstname', existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        'speakers_calls', 'announcement', existing_type=sa.TEXT(), nullable=True
    )
    op.alter_column('social_links', 'link', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('sessions', 'title', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        'event_copyrights', 'licence', existing_type=sa.VARCHAR(), nullable=True
    )
    # end Alembic commands #
