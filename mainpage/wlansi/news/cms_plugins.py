from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

class NewsPlugin(plugin_base.CMSPluginBase):
    """
    This plugin provides form for visitors to subscribe to news mailing list.
    """

    module = 'wlan slovenija'
    name = _("News")
    render_template = 'news/form.html'

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(NewsPlugin)
