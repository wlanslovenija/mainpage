from __future__ import absolute_import

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views import main
from django.db.models import aggregates
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from . import models

class HasPaperListFilter(admin.SimpleListFilter):
    title = _("has paper")
    parameter_name = 'haspaper'

    def lookups(self, request, model_admin):
        return (
            ('1', _("Yes")),
            ('0', _("No")),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(papers_count=aggregates.Count('papers'))
        if self.value() == '1':
            return queryset.exclude(papers_count=0)
        if self.value() == '0':
            return queryset.filter(papers_count=0)

class HasFinalPaperListFilter(admin.SimpleListFilter):
    title = _("has final paper")
    parameter_name = 'hasfinalpaper'

    def lookups(self, request, model_admin):
        return (
            ('1', _("Yes")),
            ('0', _("No")),
        )

    def queryset(self, request, queryset):
        # TODO: Rewrite to use conditional annotates when https://code.djangoproject.com/ticket/11305
        count = """(SELECT COUNT(*) FROM wlansi_transactionpaper WHERE wlansi_transactionpaper.is_final=1 AND wlansi_transactionpaper.transaction_id=wlansi_transaction.id)"""
        if self.value() == '1':
            return queryset.extra(where=(
               '%s!=0' % count,
            ))
        if self.value() == '0':
            return queryset.extra(where=(
               '%s=0' % count,
            ))

class BlankChoicesFieldListFilter(admin.ChoicesFieldListFilter):
    def choices(self, cl):
        for choice in super(BlankChoicesFieldListFilter, self).choices(cl):
            yield choice
        yield {
            'selected': self.lookup_val == '',
            'query_string': cl.get_query_string({self.lookup_kwarg: ''}),
            'display': main.EMPTY_CHANGELIST_VALUE,
        }

admin.FieldListFilter.register(lambda f: bool(f.choices) and f.blank, BlankChoicesFieldListFilter, True)

titles = tuple('title_%s' % language_code for language_code, language_name in settings.LANGUAGES)

class FundingSourceAdmin(admin.ModelAdmin):
    list_display = titles
    list_display_links = titles
    search_fields = titles + ('internal_comment',)

admin.site.register(models.FundingSource, FundingSourceAdmin)

descriptions = tuple('description_%s' % language_code for language_code, language_name in settings.LANGUAGES)

class PaperInline(admin.StackedInline):
    model = models.TransactionPaper
    extra = 0

# TODO: We could also filter by amount ranges

class TransactionAdmin(admin.ModelAdmin):
    inlines = (
        PaperInline,
    )
    date_hierarchy = 'date'
    list_display = ('amount',)
    list_display_links = ('amount',)
    list_filter = ('date', 'funding_source', HasPaperListFilter, HasFinalPaperListFilter, 'reimbursed')
    search_fields = ('date', 'amount') + descriptions + ('internal_comment',)

    def get_list_display(self, request):
        language = translation.get_language()

        # We have to do all this because we want column to be ordered by current language title and not funding source pk
        def funding_source(obj):
            return getattr(obj.funding_source, 'title_%s' % language)
        funding_source.admin_order_field = 'funding_source__title_%s' % language

        return descriptions + self.list_display + ('date', funding_source, 'has_paper', 'has_final_paper', 'reimbursed')

admin.site.register(models.Transaction, TransactionAdmin)
