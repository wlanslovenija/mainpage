import decimal

from django.conf import settings
from django.core import validators
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

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
