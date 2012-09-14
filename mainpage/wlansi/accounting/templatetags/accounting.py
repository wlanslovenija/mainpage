from __future__ import absolute_import

import decimal, itertools

from django import template

from ...donations import models as donations_models

from .. import models

register = template.Library()

@register.inclusion_tag('accounting/templatetag_summary.html')
def year_summary(year):
    year = int(year)

    income = decimal.Decimal(0)
    expenditure = decimal.Decimal(0)
    balance = decimal.Decimal(0)

    for transaction in itertools.chain(models.Transaction.objects.all(), donations_models.Donation.objects.all()):
        if transaction.date.year < year:
            balance += transaction.amount
        elif transaction.date.year == year:
            balance += transaction.amount
            if transaction.amount > 0:
                income += transaction.amount
            else:
                expenditure -= transaction.amount

    return {
        'income': income,
        'expenditure': expenditure,
        'balance': balance,
    }
