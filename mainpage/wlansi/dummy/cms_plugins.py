from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from . import models

class DummyPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a dummy content.
    """

    module = 'wlan slovenija'
    model = models.Dummy
    name = _("Dummy")
    render_template = 'dummy/dummy.html'

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context

plugin_pool.register_plugin(DummyPlugin)
