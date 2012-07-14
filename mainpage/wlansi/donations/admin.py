from __future__ import absolute_import

from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from . import models

class IsAnonymousListFilter(admin.SimpleListFilter):
    title = _("is anonymous")
    parameter_name = 'isanonymous'

    def lookups(self, request, model_admin):
        return (
            ('1', _("Yes")),
            ('0', _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(Q(donor__isnull=True) | Q(donor__exact=''))
        if self.value() == '0':
            return queryset.exclude(donor__isnull=True).exclude(donor__exact='')

# TODO: We could also filter by amount ranges

class DonationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('donor', 'amount', 'date', 'is_anonymous')
    list_display_links = ('amount',)
    list_filter = ('date', IsAnonymousListFilter)
    search_fields = ('date', 'amount', 'donor', 'message', 'internal_comment')

admin.site.register(models.Donation, DonationAdmin)
