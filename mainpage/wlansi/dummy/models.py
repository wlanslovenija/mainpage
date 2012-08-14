from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import pluginmodel

class Dummy(pluginmodel.CMSPlugin):
    width = models.CharField(max_length=100, help_text=_("Width of the dummy content, in CSS format."))
    height = models.CharField(max_length=100, help_text=_("Height of the dummy content, in CSS format."))
    content = models.TextField(blank=True)

    class Meta:
        verbose_name = _("dummy")
        verbose_name_plural = _("dummies")

    def __unicode__(self):
        return unicode(_(u"%(width)sx%(height)s dummy (%(content)s)" % {'width': self.width, 'height': self.height, 'content': self.content}))
