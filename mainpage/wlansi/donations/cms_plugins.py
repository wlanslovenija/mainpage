from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from . import models

class DonationsPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a list of donations.
    """

    module = 'wlan slovenija'
    name = _("Donations")
    render_template = 'donations/list.html'

    def render(self, context, instance, placeholder):
        context.update({
            'donations': models.Donation.objects.all(),
        })
        return context

plugin_pool.register_plugin(DonationsPlugin)
