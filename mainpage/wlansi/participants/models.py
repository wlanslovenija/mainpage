from django.contrib.auth import models as auth_models
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _

SOURCE_CHOICES = (
    ('manual', _("Manually added")),
    ('git', _("Git source code")),
    ('trac', _("Trac wiki and tickets")),
)

class Participant(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True, help_text=_("Full name, nickname, username, etc. Make sure you verify how and if person wants to be listed among participants."))
    source = models.CharField(max_length=6, choices=SOURCE_CHOICES, editable=False, default=SOURCE_CHOICES[0][0])
    internal_comment = models.TextField(help_text=_("Internal comment, description, reason, circumstances, etc."))
    duplicate_of = models.ForeignKey('self', blank=True, null=True)
    user = models.ForeignKey(auth_models.User, blank=True, null=True)

    class Meta:
        verbose_name = _("participant")
        verbose_name_plural = _("participants")
        ordering = ('name',)
        app_label = 'wlansi'

    def __unicode__(self):
        return u'%s' % self.name
    
    def clean(self):
        if self.duplicate_of and self.user:
            raise exceptions.ValidationError("Only one of 'duplicate of' or 'user' can be set.")

        if not self.pk:
            return

        duplicate = self.duplicate_of
        while duplicate is not None:
            if duplicate.pk == self.pk:
                raise exceptions.ValidationError("There is a dependency cycle.")
            duplicate = duplicate.duplicate_of
