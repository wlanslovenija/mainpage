import decimal

from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from cms import plugin_base

from paypal.standard.ipn import models as ipn_models
from paypal.standard.pdt import models as pdt_models

STATE_CHOICES = (
    ('pending', _("Pending")),
    ('invalid', _("Invalid")),
    ('canceled', _("Canceled")),
    ('processing', _("Processing")),
    ('sent', _("Sent")),
    ('delivered', _("Delivered")),
    ('online', _("Online")),
    ('test', _("Test")),
)

class BuyNow(plugin_base.CMSPlugin):
    item_name = models.CharField(max_length=127, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[validators.MinValueValidator(decimal.Decimal('0.01'))], help_text=_("In EUR, with all processing costs but without shipping, amount to charge per unit."))
    weight = models.DecimalField(max_digits=12, decimal_places=2, validators=[validators.MinValueValidator(decimal.Decimal('0.01'))], help_text=_("In kg, per unit, with all packaging and extra content."))

    def __unicode__(self):
        return self.item_name

class Order(models.Model):
    txn_id = models.CharField(_("transaction ID"), max_length=19, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(BuyNow, blank=False, null=False)
    quantity = models.IntegerField()
    order_by = models.CharField(max_length=129)
    email = models.CharField(_("e-mail address"), max_length=129)
    phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    handling = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pdt = models.ForeignKey(pdt_models.PayPalPDT, verbose_name="PDT", blank=True, null=True)
    ipn = models.ForeignKey(ipn_models.PayPalIPN, verbose_name="IPN", blank=True, null=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, help_text=_("What is the state of this order?"), default='pending')
    node_name = models.CharField(max_length=255, blank=True)
    internal_comment = models.TextField(blank=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ('-timestamp',)
        app_label = 'wlansi'

    def __unicode__(self):
        return unicode(_(u"%(quantity)sx%(item)s/%(state)s" % {'quantity': self.quantity, 'item': self.item, 'state': self.get_state_display()}))
