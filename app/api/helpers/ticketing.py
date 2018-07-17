from datetime import datetime

from flask_login import current_user

from app.api.helpers.db import save_to_db, get_count
from app.api.helpers.files import make_frontend_url
from app.api.helpers.mail import send_email_to_attendees
from app.api.helpers.notification import send_notif_to_attendees, send_notif_ticket_purchase_organizer
from app.api.helpers.order import delete_related_attendees_for_order
from app.api.helpers.payment import StripePaymentsManager, PayPalPaymentsManager
from app.models import db
from app.models.ticket_fee import TicketFees
from app.models.ticket_holder import TicketHolder


class TicketingManager(object):
    """All ticketing and orders related helper functions"""

    @staticmethod
    def get_order_expiry():
        return 10

    @staticmethod
    def match_discount_quantity(discount_code, ticket_holders=None):
        qty = 0
        old_holders = get_count(TicketHolder.query.filter(TicketHolder.ticket_id.in_(discount_code.tickets.split(","))))

        for holder in ticket_holders:
            ticket_holder = TicketHolder.query.filter_by(id=holder).one()
            if ticket_holder.ticket.id in discount_code.tickets.split(","):
                qty += 1
        if (qty+old_holders) <= discount_code.tickets_number and \
           discount_code.min_quantity <= qty <= discount_code.max_quantity:
            return True

        return False

    @staticmethod
    def calculate_update_amount(order):
        discount = None
        if order.discount_code_id:
            discount = order.discount_code
        # Access code part will be done ticket_holders API
        amount = 0
        total_discount = 0
        fees = TicketFees.query.filter_by(currency=order.event.payment_currency).first()

        for order_ticket in order.order_tickets:
            with db.session.no_autoflush:
                if order_ticket.ticket.is_fee_absorbed or not fees:
                    ticket_amount = (order_ticket.ticket.price * order_ticket.quantity)
                    amount += (order_ticket.ticket.price * order_ticket.quantity)
                else:
                    order_fee = fees.service_fee * (order_ticket.ticket.price * order_ticket.quantity) / 100
                    if order_fee > fees.maximum_fee:
                        ticket_amount = (order_ticket.ticket.price * order_ticket.quantity) + fees.maximum_fee
                        amount += (order_ticket.ticket.price * order_ticket.quantity) + fees.maximum_fee
                    else:
                        ticket_amount = (order_ticket.ticket.price * order_ticket.quantity) + order_fee
                        amount += (order_ticket.ticket.price * order_ticket.quantity) + order_fee

                if discount and str(order_ticket.ticket.id) in discount.tickets.split(","):
                    if discount.type == "amount":
                        total_discount += discount.value * order_ticket.quantity
                    else:
                        total_discount += discount.value * ticket_amount / 100

        if discount:
            if discount.type == "amount":
                order.amount = max(amount - total_discount, 0)
            elif discount.type == "percent":
                order.amount = amount - (discount.value * amount / 100.0)
        else:
            order.amount = amount
        save_to_db(order)
        return order

    @staticmethod
    def charge_stripe_order_payment(order, token_id):
        """
        Charge the user through Stripe
        :param order: Order for which to charge for
        :param token_id: Stripe token
        :return:
        """
        # save the stripe token with the order
        order.stripe_token = token_id
        save_to_db(order)

        # charge the user
        charge = StripePaymentsManager.capture_payment(order)

        # charge.paid is true if the charge succeeded, or was successfully authorized for later capture.
        if charge.paid:
            # update the order in the db.
            order.paid_via = 'stripe'
            order.payment_mode = charge.source.object
            order.brand = charge.source.brand
            order.exp_month = charge.source.exp_month
            order.exp_year = charge.source.exp_year
            order.last4 = charge.source.last4
            order.transaction_id = charge.id
            order.status = 'completed'
            order.completed_at = datetime.utcnow()
            save_to_db(order)

            # send email and notifications
            send_email_to_attendees(order, current_user.id)
            send_notif_to_attendees(order, current_user.id)

            order_url = make_frontend_url(path='/orders/{identifier}'.format(identifier=order.identifier))
            for organizer in order.event.organizers:
                send_notif_ticket_purchase_organizer(organizer, order.invoice_number, order_url, order.event.name)

            return True, order
        else:
            # payment failed hence expire the order
            order.status = 'expired'
            save_to_db(order)

            # delete related attendees to unlock the tickets
            delete_related_attendees_for_order(order)

            # return the failure message from stripe.
            return False, charge.failure_message

    @staticmethod
    def charge_paypal_order_payment(order, token_id):
        """
        Charge the user through paypal.
        :param order: Order for which to charge for
        :param token_id: Paypal token
        :return:
        """
        # save the paypal token with the order
        order.paypal_token = token_id
        save_to_db(order)

        # get relevant details from Paypal using the token
        payment_details = PayPalPaymentsManager.get_approved_payment_details(order)

        # charge the user
        if 'PAYERID' in payment_details:
            capture_result = PayPalPaymentsManager.capture_payment(order, payment_details['PAYERID'])
            if capture_result['ACK'] == 'Success':
                order.paid_via = 'paypal'
                order.status = 'completed'
                order.transaction_id = capture_result['PAYMENTINFO_0_TRANSACTIONID']
                order.completed_at = datetime.utcnow()
                save_to_db(order)

                # send email and notifications
                send_email_to_attendees(order, current_user.id)
                send_notif_to_attendees(order, current_user.id)

                order_url = make_frontend_url(path='/orders/{identifier}'.format(identifier=order.identifier))
                for organizer in order.event.organizers:
                    send_notif_ticket_purchase_organizer(organizer, order.invoice_number, order_url, order.event.name)

                return True, order
            else:
                # payment failed hence expire the order
                order.status = 'expired'
                save_to_db(order)

                # delete related attendees to unlock the tickets
                delete_related_attendees_for_order(order)

                # return the error message from Paypal
                return False, capture_result['L_SHORTMESSAGE0']
        else:
            return False, 'Payer ID missing. Payment flow tampered.'
