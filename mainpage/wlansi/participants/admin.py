from __future__ import absolute_import

from django.contrib import admin
from django.db import models as django_models

from . import models

# TODO: We could also filter by duplicate or not

class ParticipantAdmin(admin.ModelAdmin):
    date_hierarchy = 'added'
    list_display = ('name', 'source', 'added', 'duplicate_of')
    list_filter = ('added', 'source')
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
