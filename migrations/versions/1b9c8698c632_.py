"""empty message

Revision ID: 1b9c8698c632
Revises: af9215895b80
Create Date: 2017-06-15 22:39:27.240374

"""

# revision identifiers, used by Alembic.
revision = '1b9c8698c632'
down_revision = 'af9215895b80'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


class ReplaceableObject(object):
    def __init__(self, name, sqltext):
        self.name = name
        self.sqltext = sqltext


# function to find a and replace a string(the whole string should match, not substring)
# across all the columns of a table.
# If run is true then the function executes the query.
# This will work only for nullable columns
replace_in_table = ReplaceableObject(
    "replace_in_table(table_name text, original text, replacement text, run boolean)",
    """
    returns text language plpgsql
    as $$
    declare
        r record;
        q text;
    begin
        q = '';
        for r in
            select attname
            from pg_attribute
            where attrelid = table_name::regclass
                and attnum > 0
                and not attisdropped
                and (atttypid = 25
                or atttypid = 1042
                or atttypid = 1043)
                and not attnotnull
            order by attnum
        loop
            q = format($fmt$%supdate %s set %s = %s where %s = %s;$fmt$,
                q, table_name, r.attname, replacement, r.attname, original);
        end loop;
        q = format('%s;', rtrim(q, ';'));
        if run then
            execute q;
        end if;
        return q;
    end $$;
    """,
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_or_replace_sp(replace_in_table)
    op.alter_column('social_links', 'link', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('sessions', 'title', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        'sessions_version', 'title', existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        'call_for_papers', 'announcement', existing_type=sa.VARCHAR(), nullable=True
    )

    # to create these statements automatically, please print them like
    # print("""op.execute("SELECT replace_in_table('""" + table[0] + """', '''''', 'NULL', true)",
    #           execution_options=None)""")
    # inside the function to fetch all tables and models in the views directory
    # TRY AS HARD AS YOU CAN TO NOT BRING THE APP LOGIC IN MIGRATIONS
    op.execute(
        "SELECT replace_in_table('event_copyrights', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('mails', '''''', 'NULL', true)", execution_options=None
    )
    op.execute(
        "SELECT replace_in_table('social_links', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('booked_ticket', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('tax', '''''', 'NULL', true)", execution_options=None
    )
    op.execute(
        "SELECT replace_in_table('custom_sys_roles', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('custom_forms', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('microlocations', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('user_permissions', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('event_user', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('orders', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('orders_tickets', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('discount_codes', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('ticket_fees', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('access_codes', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('user_system_role', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('message_settings', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('image_sizes', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('speaker', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('stripe_authorizations', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('role_invites', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('custom_placeholders', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('session_types', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('events', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('activities', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('users', '''''', 'NULL', true)", execution_options=None
    )
    op.execute(
        "SELECT replace_in_table('sessions', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('sponsors', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('ticket_holders', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('notifications', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('tracks', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('users_events_roles', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('email_notifications', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('services', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('export_jobs', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('image_config', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('pages', '''''', 'NULL', true)", execution_options=None
    )
    op.execute(
        "SELECT replace_in_table('permissions', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('tickets', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('roles', '''''', 'NULL', true)", execution_options=None
    )
    op.execute(
        "SELECT replace_in_table('settings', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('versions', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('modules', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('event_invoices', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('import_jobs', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('call_for_papers', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('panel_permissions', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('ticket_tag', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('invites', '''''', 'NULL', true)",
        execution_options=None,
    )

    op.execute(
        "SELECT replace_in_table('sessions_version', '''''', 'NULL', true)",
        execution_options=None,
    )
    op.execute(
        "SELECT replace_in_table('events_version', '''''', 'NULL', true)",
        execution_options=None,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_sp(replace_in_table)
    op.alter_column('social_links', 'link', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('sessions', 'title', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        'sessions_version', 'title', existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        'call_for_papers', 'announcement', existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###
