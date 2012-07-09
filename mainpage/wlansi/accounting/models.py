from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from filer.fields import file

class FundingSourceMetaclass(models.Model.__metaclass__):
    def __new__(cls, name, bases, attrs):
        for language_code, language_name in settings.LANGUAGES:
            attrs['title_%s' % language_code] = models.CharField(max_length=255)
        attrs['internal_comment'] = models.TextField(blank=True, help_text=_("Internal comment, like conditions, etc."))
        return super(FundingSourceMetaclass, cls).__new__(cls, name, bases, attrs)

class FundingSource(models.Model):
    __metaclass__ = FundingSourceMetaclass

    class Meta:
        verbose_name = _("funding source")
        verbose_name_plural = _("funding sources")
        ordering = ('id',)
        app_label = 'wlansi'

    def __unicode__(self):
        language = translation.get_language()
        return getattr(self, 'title_%s' % language)

class TransactionMetaclass(models.Model.__metaclass__):
    def __new__(cls, name, bases, attrs):
        for language_code, language_name in settings.LANGUAGES:
            attrs['description_%s' % language_code] = models.TextField(help_text=_("You can use Trac formatting."))
        return super(TransactionMetaclass, cls).__new__(cls, name, bases, attrs)

class Transaction(models.Model):
    __metaclass__ = TransactionMetaclass

    funding_source = models.ForeignKey(FundingSource, related_name='transactions')
    date = models.DateField(help_text=_("Date of transaction on the account."))
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text=_("In EUR, final amount on the account."))
    internal_comment = models.TextField(blank=True, help_text=_("Internal comment, like circumstances, etc."))

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        ordering = ('-date',)
        app_label = 'wlansi'

    def get_description(self):
        language = translation.get_language()
        return getattr(self, 'description_%s' % language)

    def __unicode__(self):
        return unicode(_(u"%(amount)s on %(date)s" % {'amount': self.amount, 'date': self.date}))

class TransactionPaper(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='papers')
    is_final = models.BooleanField(help_text=_("Is this paper final version for transaction?")) 
    paper = file.FilerFileField(help_text=_("Bills, invoices, estimates, calculations, and other statements connected with transaction."))

    class Meta:
        verbose_name = _("paper")
        verbose_name_plural = _("papers")
        app_label = 'wlansi'

    def __unicode__(self):
        return unicode(self.paper)
