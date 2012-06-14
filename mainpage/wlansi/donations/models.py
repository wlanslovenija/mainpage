from django.db import models
from django.utils.translation import ugettext_lazy as _

class Donation(models.Model):
    date = models.DateField(help_text=_("Date of donation on the account."))
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text=_("In EUR, without any processing costs, final amount on the account."))
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
