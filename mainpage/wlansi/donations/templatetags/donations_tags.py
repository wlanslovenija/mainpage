import decimal

from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return decimal.Decimal(value) - decimal.Decimal(arg)
