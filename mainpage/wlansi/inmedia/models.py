from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields import file

from frontend.account import geo_fields

class Entry(models.Model):
    date = models.DateField()
    link = models.URLField(blank=True, help_text=_("URL of official publication, if available."))
    local_copy = file.FilerFileField(blank=True, null=True, help_text=_("Because official publications often disappear, we try to make also local copies (PDFs, audio and video recordings, etc.)."))

    def has_link(self):
        return bool(self.link)
    has_link.boolean = True

    def has_local_copy(self):
        return bool(self.local_copy)
    has_local_copy.boolean = True

    def source(self):
        return self.descriptions.all()[0].source
    source.admin_order_field = 'descriptions__source'

    def languages(self):
        return ', '.join([desc.get_language_display() for desc in self.descriptions.all()])

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")
        ordering = ('-date',)

class Description(models.Model):
    entry = models.ForeignKey(Entry, related_name='descriptions')
    language = geo_fields.LanguageField()
    source = models.CharField(max_length=255, help_text=_("Name of the publication source. In chosen language, if possible."))
    description = models.TextField(help_text=_("You can use Trac formatting."))

    def __unicode__(self):
        return unicode(_(u"for language %(language)s" % {'language': self.get_language_display()}))
