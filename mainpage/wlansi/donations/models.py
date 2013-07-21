import decimal

from django.conf import settings
from django.core import validators
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from cms import plugin_base

from paypal.standard.ipn import models as ipn_models
from paypal.standard.pdt import models as pdt_models

class Donate(plugin_base.CMSPlugin):
    organization_name_or_service = models.CharField(max_length=127)
    # We do not allow numerical donation IDs because we are using such IDs for shop items
    donation_id = models.CharField(max_length=127, validators=[validators.RegexValidator(r'\D')])

    def __unicode__(self):
        return unicode(_(u"%(organization_name_or_service)s/%(donation_id)s" % {'organization_name_or_service': self.organization_name_or_service, 'donation_id': self.donation_id}))

class DonationSourceMetaclass(models.Model.__metaclass__):
    def __new__(cls, name, bases, attrs):
        for language_code, language_name in settings.LANGUAGES:
            attrs['title_%s' % language_code] = models.CharField(max_length=255)
        attrs['internal_comment'] = models.TextField(blank=True)
        return super(DonationSourceMetaclass, cls).__new__(cls, name, bases, attrs)

class DonationSource(models.Model):
    __metaclass__ = DonationSourceMetaclass

    class Meta:
        verbose_name = _("donation source")
        verbose_name_plural = _("donation sources")
        ordering = ('id',)
        app_label = 'wlansi'

    def __unicode__(self):
        language = translation.get_language()
        return getattr(self, 'title_%s' % language)

class Donation(models.Model):
    donation_source = models.ForeignKey(DonationSource, blank=True, null=True, related_name='donations')
    date = models.DateField(help_text=_("Date of donation on the account."))
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[validators.MinValueValidator(decimal.Decimal('0.01'))], help_text=_("In EUR, without any processing costs, final amount on the account."))
    donor = models.CharField(max_length=255, blank=True, help_text=_("Leave blank if anonymous."))
    message = models.TextField(blank=True)
    internal_comment = models.TextField(blank=True, help_text=_("Internal comment, like donation source, circumstances, etc."))

    txn_id = models.CharField(_("transaction ID"), max_length=19, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    donation_by = models.CharField(max_length=129, blank=True)
    email = models.CharField(_("e-mail address"), max_length=129, blank=True)
    gross = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    pdt = models.ForeignKey(pdt_models.PayPalPDT, verbose_name="PDT", blank=True, null=True)
    ipn = models.ForeignKey(ipn_models.PayPalIPN, verbose_name="IPN", blank=True, null=True)

    class Meta:
        verbose_name = _("donation")
        verbose_name_plural = _("donations")
        ordering = ('-date',)
        app_label = 'wlansi'

    def is_anonymous(self):
        return not bool(self.donor)
    is_anonymous.boolean = True

    def __unicode__(self):
        return unicode(_(u"%(amount)s on %(date)s" % {'amount': self.amount, 'date': self.date}))
