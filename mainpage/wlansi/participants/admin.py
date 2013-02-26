from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

import reversion

from . import models

class DuplicateListFilter(admin.SimpleListFilter):
    title = _("is duplicate")
    parameter_name = 'duplicate'

    def lookups(self, request, model_admin):
        return (
            ('1', _("Yes")),
            ('0', _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(duplicate_of__isnull=False)
        if self.value() == '0':
            return queryset.filter(duplicate_of__isnull=True)

class ParticipantAdmin(reversion.VersionAdmin):
    date_hierarchy = 'added'
    list_display = ('name', 'source', 'added', 'duplicate_of')
    list_filter = ('added', 'source', DuplicateListFilter)
    search_fields = ('name', 'source', 'internal_comment')

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ParticipantAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if formfield:
            # Hiddes adding related object, it is a bit strange to allow adding of duplicate or user, we want only selection
            formfield.widget.can_add_related = False
        return formfield

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            # Only on edit view we allow setting a duplicate or user (why would you be creating a duplicate in the first place?)
            kwargs['exclude'] = ('duplicate_of', 'user')
        return super(ParticipantAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(models.Participant, ParticipantAdmin)
