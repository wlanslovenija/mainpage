from __future__ import absolute_import

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db.models import aggregates
from django.forms import models as models_forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from . import models

class HasLinkListFilter(admin.SimpleListFilter):
    title = _("has link")
    parameter_name = 'haslink'

    def lookups(self, request, model_admin):
        return (
            ('1', _("Yes")),
            ('0', _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.exclude(link__isnull=True).exclude(link__exact='')
        if self.value() == '0':
            return queryset.filter(Q(link__isnull=True) | Q(link__exact=''))

class HasLocalCopyListFilter(admin.SimpleListFilter):
    title = _("has local copy")
    parameter_name = 'haslocalcopy'

    def lookups(self, request, model_admin):
        return (
            ('1', _("Yes")),
            ('0', _("No")),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(local_copies_count=aggregates.Count('local_copies'))
        if self.value() == '1':
            return queryset.exclude(local_copies_count=0)
        if self.value() == '0':
            return queryset.filter(local_copies_count=0)

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
            raise forms.ValidationError(_("At least one %(name)s is required." % {'name': unicode(self.model._meta.verbose_name)}))

class InitialLanguagesFormSet(RequireOneFormSet):
    """
    Sets initial languages to not yet existing languages in the formset.
    """

    def _construct_form(self, i, **kwargs):
        if i >= self.initial_form_count():
            existing = self.queryset.values_list('language', flat=True)
            initial = [{'language': language_code} for language_code, language_name in settings.LANGUAGES if language_code not in existing]
            try:
                kwargs['initial'] = initial[i-self.initial_form_count()]
            except IndexError:
                pass
        return super(InitialLanguagesFormSet, self)._construct_form(i, **kwargs)

class DescriptionInline(admin.StackedInline):
    model = models.InMediaDescription
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)
    formset = InitialLanguagesFormSet

class LocalCopyInline(admin.StackedInline):
    model = models.InMediaLocalCopy
    extra = 1

class EntryAdmin(admin.ModelAdmin):
    inlines = (
        LocalCopyInline,
        DescriptionInline,
    )
    date_hierarchy = 'date'
    list_display = ('source', 'date', 'languages', 'has_link', 'has_local_copy')
    list_filter = ('date', 'descriptions__language', HasLinkListFilter, HasLocalCopyListFilter)
    search_fields = ('date', 'descriptions__language', 'descriptions__source', 'descriptions__description')

admin.site.register(models.InMediaEntry, EntryAdmin)
