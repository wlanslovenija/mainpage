from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

class TransactionMetaclass(models.Model.__metaclass__):
    def __new__(cls, name, bases, attrs):
        for language_code, language_name in settings.LANGUAGES:
            attrs['description_%s' % language_code] = models.TextField(help_text=_("You can use Trac formatting."))
        return super(TransactionMetaclass, cls).__new__(cls, name, bases, attrs)

class Transaction(models.Model):
    __metaclass__ = TransactionMetaclass

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
