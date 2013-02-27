from django.contrib import admin
from django.contrib.admin.templatetags import admin_static
from django.core import urlresolvers
from django.db.models.fields import related
from django.forms import widgets
from django.utils import safestring
from django.utils.translation import ugettext_lazy as _

from paypal.standard.ipn import admin as ipn_admin, models as ipn_models
from paypal.standard.pdt import admin as pdt_admin, models as pdt_models

import reversion

from . import models

class LinkedSelect(widgets.Select):
    def render(self, name, value, attrs=None, *args, **kwargs):
        output = [super(LinkedSelect, self).render(name, value, attrs=attrs, *args, **kwargs)]

        model = self.choices.field.queryset.model
        try:
            obj = model.objects.get(id=value)
            change_url = urlresolvers.reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.object_name.lower()), args=(obj.pk,))
            output.append(u'<a href="%s" class="change-object" id="change_id_%s"> ' % (change_url, name))
            output.append(u'<img src="%s" width="10" height="10" alt="%s"/></a>' % (admin_static.static('admin/img/icon_changelink.gif'), _('Change Object')))
        except (model.DoesNotExist, urlresolvers.NoReverseMatch):
            pass

        return safestring.mark_safe(u''.join(output))

class OrderAdmin(reversion.VersionAdmin):
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    list_display = ('txn_id', 'timestamp', 'item', 'quantity', 'order_by', 'email', 'phone', 'gross', 'fee', 'shipping', 'handling', 'node_name', 'state')
    list_display_links = ('txn_id',)
    list_filter = ('timestamp', 'item', 'quantity', 'state')
    search_fields = ('item__item_name', 'email', 'phone', 'shipping_address', 'internal_comment')
    formfield_overrides = {
        related.ForeignKey: {
            'widget': LinkedSelect,
        },
    }

admin.site.register(models.Order, OrderAdmin)

class PayPalPDTAdmin(pdt_admin.PayPalPDTAdmin, reversion.VersionAdmin):
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_filter = ('created_at', 'payment_status', 'flag')

    def has_add_permission(self, request):
        return False

admin.site.unregister(pdt_models.PayPalPDT)
admin.site.register(pdt_models.PayPalPDT, PayPalPDTAdmin)

class PayPalIPNAdmin(ipn_admin.PayPalIPNAdmin, reversion.VersionAdmin):
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_filter = ('created_at', 'payment_status', 'flag')

    def has_add_permission(self, request):
        return False

admin.site.unregister(ipn_models.PayPalIPN)
admin.site.register(ipn_models.PayPalIPN, PayPalIPNAdmin)
