"""empty message

Revision ID: d512ae8422a0
Revises: abad6f635a43
Create Date: 2020-10-13 17:03:26.431761

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'd512ae8422a0'
down_revision = 'abad6f635a43'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('drop table if exists invites')
    op.execute('update events set can_pay_by_alipay = false where can_pay_by_alipay is null')
    op.alter_column('events', 'can_pay_by_alipay',
               nullable=False,
               server_default='False')
    op.execute('update events set can_pay_by_bank = false where can_pay_by_bank is null')
    op.alter_column('events', 'can_pay_by_bank',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default='False')
    op.execute('update events set can_pay_by_cheque = false where can_pay_by_cheque is null')
    op.alter_column('events', 'can_pay_by_cheque',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default='False')
    op.execute('update events set can_pay_by_omise = false where can_pay_by_omise is null')
    op.alter_column('events', 'can_pay_by_omise',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default='False')
    op.execute('update events set can_pay_by_paypal = false where can_pay_by_paypal is null')
    op.alter_column('events', 'can_pay_by_paypal',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default='False')
    op.execute('update events set can_pay_by_stripe = false where can_pay_by_stripe is null')
    op.alter_column('events', 'can_pay_by_stripe',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default='False')
    op.execute('update events set can_pay_onsite = false where can_pay_onsite is null')
    op.alter_column('events', 'can_pay_onsite',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               server_default='False')
    op.execute('update events set can_pay_by_paytm = false where can_pay_by_paytm is null')
    op.alter_column('events_version', 'can_pay_by_paytm',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               autoincrement=False,
               existing_server_default=sa.text('false'))
    op.alter_column('events_version', 'is_billing_info_mandatory',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               autoincrement=False,
               existing_server_default=sa.text('false'))
    op.alter_column('events_version', 'is_ticket_form_enabled',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               autoincrement=False,
               existing_server_default=sa.text('true'))
    op.alter_column('events_version', 'show_remaining_tickets',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               autoincrement=False,
               existing_server_default=sa.text('false'))
    op.execute('alter table orders drop column if exists is_reminder_mail_sent')
    op.alter_column('speaker', 'sponsorship_required',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('speaker', 'sponsorship_required',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.add_column('orders', sa.Column('is_reminder_mail_sent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('events_version', 'show_remaining_tickets',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               autoincrement=False,
               existing_server_default=sa.text('false'))
    op.alter_column('events_version', 'is_ticket_form_enabled',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               autoincrement=False,
               existing_server_default=sa.text('true'))
    op.alter_column('events_version', 'is_billing_info_mandatory',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               autoincrement=False,
               existing_server_default=sa.text('false'))
    op.alter_column('events_version', 'can_pay_by_paytm',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               autoincrement=False,
               existing_server_default=sa.text('false'))
    op.alter_column('events', 'can_pay_onsite',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('events', 'can_pay_by_stripe',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('events', 'can_pay_by_paypal',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('events', 'can_pay_by_omise',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('events', 'can_pay_by_cheque',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('events', 'can_pay_by_bank',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('events', 'can_pay_by_alipay',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.create_table('invites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('session_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('hash', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], name='invites_event_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], name='invites_session_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='invites_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='invites_pkey')
    )
    # ### end Alembic commands ###
