import decimal

from django.conf import settings
from django.contrib import admin
from django.db.models import Q
from django.db.models.fields import related
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

import reversion

from ..buynow import admin as buynow_admin

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

titles = tuple('title_%s' % language_code for language_code, language_name in settings.LANGUAGES)

class DonationSourceAdmin(admin.ModelAdmin):
    list_display = titles
    list_display_links = titles
    search_fields = titles + ('internal_comment',)

admin.site.register(models.DonationSource, DonationSourceAdmin)

class DonationAdmin(reversion.VersionAdmin):
    date_hierarchy = 'date'
    list_display = ('donor', 'amount', 'date')
    list_display_links = ('amount',)
    list_filter = ('date', 'donation_source', IsAnonymousListFilter)
    search_fields = ('date', 'amount', 'donor', 'message', 'internal_comment')
    formfield_overrides = {
        related.ForeignKey: {
            'widget': buynow_admin.LinkedSelect,
        },
    }
    fieldsets = (
        (None, {
            'fields': ('donation_source', 'date', 'amount', 'donor', 'message', 'internal_comment'),
        }),
        (_("PayPal"), {
            'fields': ('txn_id', 'timestamp', 'donation_by', 'email', 'gross', 'fee', 'pdt', 'ipn'),
        }),
    )
    actions = ('compute_summary',)

    def compute_summary(self, request, queryset):
        summary = decimal.Decimal(0)

        for donation in queryset:
            summary += donation.amount

        context = {
            'title': _("Summary"),
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'count': queryset.count(),
            'summary': summary,
        }

        return response.TemplateResponse(request, 'donations/admin_summary.html', context, current_app=self.admin_site.name)

    def get_list_display(self, request):
        language = translation.get_language()

        # We have to do all this because we want column to be ordered by current language title and not donation source pk
        def donation_source(obj):
            return getattr(obj.donation_source, 'title_%s' % language)
        donation_source.admin_order_field = 'donation_source__title_%s' % language

        return self.list_display + (donation_source, 'is_anonymous')

admin.site.register(models.Donation, DonationAdmin)
