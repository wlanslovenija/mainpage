from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from filer.fields import file

from frontend.account import geo_fields

class InMediaEntry(models.Model):
    date = models.DateField()
    link = models.URLField(blank=True, help_text=_("URL of official publication, if available."))

    class Meta:
        verbose_name = _("in media entry")
        verbose_name_plural = _("in media entries")
        ordering = ('-date',)
        app_label = 'wlansi'

    def has_link(self):
        return bool(self.link)
    has_link.boolean = True

    def has_local_copy(self):
        return bool(self.local_copies.count())
    has_local_copy.boolean = True

    def source(self):
        # We assume each entry has at least one description (enforced by admin)
        return self.descriptions.all()[0].source
    source.admin_order_field = 'descriptions__source'

    def languages(self):
        return ', '.join([desc.get_language_display() for desc in self.descriptions.all()])

    def get_language(self):
        language = translation.get_language()
        return self.descriptions.get(language=language)

    def __unicode__(self):
        return unicode(_(u"%(source)s on %(date)s" % {'source': self.source(), 'date': self.date}))

class InMediaLocalCopy(models.Model):
    entry = models.ForeignKey(InMediaEntry, related_name='local_copies')
    local_copy = file.FilerFileField(help_text=_("Because official publications often disappear, we try to make also local copies (PDFs, audio and video recordings, etc.)."))

    class Meta:
        verbose_name = _("local copy")
        verbose_name_plural = _("local copies")
        app_label = 'wlansi'

class InMediaDescription(models.Model):
    entry = models.ForeignKey(InMediaEntry, related_name='descriptions')
    language = geo_fields.LanguageField()
    source = models.CharField(max_length=255, help_text=_("Name of the publication source. In chosen language, if possible."))
    description = models.TextField(help_text=_("You can use Trac formatting."))

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        app_label = 'wlansi'

    def __unicode__(self):
        return unicode(_(u"for language %(language)s" % {'language': self.get_language_display()}))
