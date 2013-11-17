from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from . import models

class CoinwidgetPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a coinwidget button.
    """

    module = 'wlan slovenija'
    model = models.Coinwidget
    name = _("Coinwidget")
    render_template = "coinwidget/coinwidget.html"
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(CoinwidgetPlugin)
