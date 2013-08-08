import decimal, itertools, operator

from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from ..donations import models as donations_models

from . import models

class AccountPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a list of transactions on wlan slovenija bank account.
    """

    module = 'wlan slovenija'
    name = _("Account")
    render_template = 'accounting/list.html'

    def render(self, context, instance, placeholder):
        transactions = itertools.chain(models.Transaction.objects.all(), donations_models.Donation.objects.all())
        transactions = sorted(transactions, key=operator.attrgetter('date', 'id'), reverse=True)
        context.update({
            'transactions': transactions,
        })
        return context

plugin_pool.register_plugin(AccountPlugin)

class BalancePlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays current balance of wlan slovenija bank account.
    """

    module = 'wlan slovenija'
    name = _("Balance")
    render_template = 'accounting/balance.html'

    def render(self, context, instance, placeholder):
        balance = decimal.Decimal(0)
        for transaction in itertools.chain(models.Transaction.objects.all(), donations_models.Donation.objects.all()):
            balance += transaction.amount
        context.update({
            'balance': balance,
        })
        return context

plugin_pool.register_plugin(BalancePlugin)
