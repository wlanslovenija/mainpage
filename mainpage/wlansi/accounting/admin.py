from __future__ import absolute_import

from django.conf import settings
from django.contrib import admin

from . import models

# TODO: We could also filter by amount ranges

descriptions = tuple('description_%s' % language_code for language_code, language_name in settings.LANGUAGES)

class PaperInline(admin.StackedInline):
    model = models.TransactionPaper
    extra = 0

class TransactionAdmin(admin.ModelAdmin):
    inlines = (
        PaperInline,
    )
    date_hierarchy = 'date'
    list_display = descriptions + ('amount', 'date')
    list_display_links = ('amount',)
    list_filter = ('date',)
    search_fields = ('date', 'amount') + descriptions + ('internal_comment',)

admin.site.register(models.Transaction, TransactionAdmin)
