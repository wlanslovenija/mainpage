from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from . import models

class HoverAnimationPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays an on-hover animation.
    """

    module = 'wlan slovenija'
    model = models.HoverAnimation
    name = _("Hover animation")
    render_template = "hoveranimation/animation.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder
        })
        return context

plugin_pool.register_plugin(HoverAnimationPlugin)
