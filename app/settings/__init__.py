import stripe
from flask import current_app
from sqlalchemy import asc, desc
from app.models.setting import Setting
from app.models.fees import TicketFees


def get_settings():
    """
    Use this to get latest system settings
    """
    if 'custom_settings' in current_app.config:
        return current_app.config['custom_settings']
    s = Setting.query.order_by(desc(Setting.id)).first()
    if s is None:
        set_settings(secret='super secret key')
    else:
        current_app.config['custom_settings'] = make_dict(s)
    return current_app.config['custom_settings']

def get_setts():
    return Setting.query.order_by(desc(Setting.id)).first()

def set_settings(**kwargs):
    """
    Update system settings
    """

    if 'service_fee' in kwargs:
        ticket_service_fees = kwargs.get('service_fee')
        ticket_maximum_fees = kwargs.get('maximum_fee')
        from app.helpers.data_getter import DataGetter
        from app.helpers.data import save_to_db
        currencies = DataGetter.get_payment_currencies()
        ticket_fees = DataGetter.get_fee_settings()
        if not ticket_fees:
            for i, (currency, has_paypal, has_stripe) in enumerate(currencies):
                currency = currency.split(' ')[0]
                if float(ticket_maximum_fees[i]) == 0.0:
                    ticket_maximum_fees[i] = ticket_service_fees[i]
                ticket_fee = TicketFees(currency=currency,
                                        service_fee=ticket_service_fees[i],
                                        maximum_fee=ticket_maximum_fees[i])
                save_to_db(ticket_fee, "Ticket Fees settings saved")
        else:
            i = 0
            for fee in ticket_fees:
                if float(ticket_maximum_fees[i]) == 0.0:
                    ticket_maximum_fees[i] = ticket_service_fees[i]
                fee.service_fee = ticket_service_fees[i]
                fee.maximum_fee = ticket_maximum_fees[i]
                save_to_db(fee, "Fee Options Updated")
                i += 1
    else:
        setting = Setting.query.order_by(desc(Setting.id)).first()
        if not setting:
            setting = Setting(**kwargs)
        else:
            for key, value in kwargs.items():
                setattr(setting, key, value)
        from app.helpers.data import save_to_db
        save_to_db(setting, 'Setting saved')
        current_app.secret_key = setting.secret
        stripe.api_key = setting.stripe_secret_key
        current_app.config['custom_settings'] = make_dict(setting)


def make_dict(s):
    arguments = {}
    for name, column in list(s.__mapper__.columns.items()):
        if not (column.primary_key or column.unique):
            arguments[name] = getattr(s, name)
    return arguments
