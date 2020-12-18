from datetime import datetime

import humanize
import pytz
from forex_python.converter import CurrencyCodes


def humanize_helper(time):
    """Returns time passed from now in a human readable duration"""

    if not time:
        return "N/A"
    return humanize.naturaltime(datetime.now(pytz.utc) - time.astimezone(pytz.utc))


def init_filters(app):
    @app.template_filter('currency_symbol')
    def currency_symbol_filter(currency_code):
        symbol = CurrencyCodes().get_symbol(currency_code)
        return symbol if symbol else currency_code

    @app.template_filter('money')
    def money_filter(string):
        return '{:20,.2f}'.format(float(string))

    @app.template_filter('datetime')
    def simple_datetime_display(date, timezone='UTC', format='%B %d, %Y %I:%M %p'):
        if not date:
            return ''
        return date.astimezone(pytz.timezone(timezone)).strftime(format)

    @app.template_filter('date')
    def simple_date_display(date, timezone='UTC'):
        return simple_datetime_display(date, timezone, '%B %d, %Y')

    @app.template_filter('humanize')
    def humanize_filter(time):
        return humanize_helper(time)
