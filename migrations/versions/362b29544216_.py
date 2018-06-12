"""empty message

Revision ID: 362b29544216
Revises: 49f3a33f5437
Create Date: 2018-06-12 08:55:12.423860

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '362b29544216'
down_revision = '49f3a33f5437'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('access_codes', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('custom_forms', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('custom_placeholders', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('discount_codes', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('email_notifications', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('event_copyrights', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('event_invoices', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('event_sub_topics', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('event_topics', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('event_types', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('faq', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('faq_types', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('feedback', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('image_sizes', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('microlocations', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('notifications', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('orders', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('orders_tickets', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('pages', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('role_invites', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('roles', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('session_types', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('social_links', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('speaker', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('speakers_calls', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('sponsors', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('stripe_authorizations', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('tax', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('ticket_fees', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('ticket_holders', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('ticket_tag', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('tickets', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('tracks', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user_permissions', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_permissions', 'deleted_at')
    op.drop_column('tracks', 'deleted_at')
    op.drop_column('tickets', 'deleted_at')
    op.drop_column('ticket_tag', 'deleted_at')
    op.drop_column('ticket_holders', 'deleted_at')
    op.drop_column('ticket_fees', 'deleted_at')
    op.drop_column('tax', 'deleted_at')
    op.drop_column('stripe_authorizations', 'deleted_at')
    op.drop_column('sponsors', 'deleted_at')
    op.drop_column('speakers_calls', 'deleted_at')
    op.drop_column('speaker', 'deleted_at')
    op.drop_column('social_links', 'deleted_at')
    op.drop_column('session_types', 'deleted_at')
    op.drop_column('roles', 'deleted_at')
    op.drop_column('role_invites', 'deleted_at')
    op.drop_column('pages', 'deleted_at')
    op.drop_column('orders_tickets', 'deleted_at')
    op.drop_column('orders', 'deleted_at')
    op.drop_column('notifications', 'deleted_at')
    op.drop_column('microlocations', 'deleted_at')
    op.drop_column('image_sizes', 'deleted_at')
    op.drop_column('feedback', 'deleted_at')
    op.drop_column('faq_types', 'deleted_at')
    op.drop_column('faq', 'deleted_at')
    op.drop_column('event_types', 'deleted_at')
    op.drop_column('event_topics', 'deleted_at')
    op.drop_column('event_sub_topics', 'deleted_at')
    op.drop_column('event_invoices', 'deleted_at')
    op.drop_column('event_copyrights', 'deleted_at')
    op.drop_column('email_notifications', 'deleted_at')
    op.drop_column('discount_codes', 'deleted_at')
    op.drop_column('custom_placeholders', 'deleted_at')
    op.drop_column('custom_forms', 'deleted_at')
    op.drop_column('access_codes', 'deleted_at')
    # ### end Alembic commands ###
