from __future__ import absolute_import

from django.conf import settings
from django.contrib import admin
from django import forms
from django.forms import models as models_forms
from django.utils.translation import ugettext_lazy as _

from . import models

# TODO: With Django 1.4, set initial values for language in descriptions to different (all supported) languages
# TODO: We could also filter by has_link and has_local_copy

# Based on: https://code.google.com/p/wadofstuff/source/browse/trunk/python/forms/wadofstuff/django/forms/forms.py
class RequireOneFormSet(models_forms.BaseInlineFormSet):
    """"
    Requires at least one form in the formset to be completed.
    """

    def clean(self):
        super(RequireOneFormSet, self).clean()

        if not self.is_valid():
            return

        completed = 0
        for cleaned_data in self.cleaned_data:
            # Form has data and we are not deleting it
            if cleaned_data and not cleaned_data.get('DELETE', False):
                completed += 1

        if completed < 1:
            raise forms.ValidationError(_("At least one %(name)s is required." % {'name': self.model._meta.verbose_name}))

class DescriptionInline(admin.StackedInline):
    model = models.Description
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)
    formset = RequireOneFormSet

class EntryAdmin(admin.ModelAdmin):
    inlines = (
        DescriptionInline,
    )
    date_hierarchy = 'date'
    list_display = ('source', 'date', 'languages', 'has_link', 'has_local_copy')
    list_filter = ('date', 'descriptions__language')
    search_fields = ('date', 'descriptions__language', 'descriptions__source', 'descriptions__description')

admin.site.register(models.Entry, EntryAdmin)
