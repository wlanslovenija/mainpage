from django.db.models import fields, validators
from django.utils.translation import ugettext_lazy as _

from cms import plugin_base

CURRENCY_CHOICES = (
    ('bitcoin', _("Bitcoin")),
    ('litecoin', _("Litecoin")),
)

COUNTER_CHOICES = (
    ('hide', _("Hide the counter")),
    ('count', _("Total number of transactions")),
    ('amount', _("Total amount received")),
)

WINDOW_ALIGNMENT_CHOICES = (
    ('bl', _("Below, left")),
    ('bc', _("Below, center")),
    ('br', _("Below, right")),
    ('al', _("Above, left")),
    ('ac', _("Above, center")),
    ('ar', _("Above, right")),
)

class Coinwidget(plugin_base.CMSPlugin):
    currency = fields.CharField(max_length=30, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0][0])
    wallet_address = fields.CharField(max_length=255)
    counter = fields.CharField(max_length=6, choices=COUNTER_CHOICES, default=COUNTER_CHOICES[0][0], help_text=_("Toggle what is shown in the counter next to the main button."))
    qr_code = fields.BooleanField(_("QR code"), default=True, help_text=_("Set to true if you want to show the QR code generator that appears at the bottom left of the window. Set to false to hide the QR code icon."))
    auto_show = fields.BooleanField(default=False, help_text=_("Set to true if you want the window to auto appear as soon as the counter finishes loading."))
    decimals = fields.SmallIntegerField(default=4, validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(10),
    ], help_text=_("Adjust the number of decimals shown on the amount received statistic."))
    button_label = fields.CharField(max_length=255, default="Donate", help_text=_("Change the text of the label on the main button."))
    address_label = fields.CharField(max_length=255, default="My Bitcoin Address:", help_text=_("The text that appears above your wallet address within the window."))
    count_label = fields.CharField(max_length=255, default="donations", help_text=_("The text that appears in the window under the total number of transactions."))
    amount_label = fields.CharField(max_length=255, default="BTC", help_text=_("The text that appears in the window under the total amount received."))
    window_alignment = fields.CharField(max_length=2, choices=WINDOW_ALIGNMENT_CHOICES, default=WINDOW_ALIGNMENT_CHOICES[0][0])
