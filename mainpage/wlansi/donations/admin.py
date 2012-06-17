from __future__ import absolute_import

from django.contrib import admin

from . import models

# TODO: We could also filter by is_anonymous and amount ranges

class DonationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('donor', 'amount', 'date', 'is_anonymous')
    list_display_links = ('amount',)
    list_filter = ('date',)
    search_fields = ('date', 'amount', 'donor', 'message', 'internal_comment')

admin.site.register(models.Donation, DonationAdmin)
