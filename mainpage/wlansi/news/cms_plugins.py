from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

class NewsPlugin(plugin_base.CMSPluginBase):
    module = 'wlan slovenija'
    name = _("News")
    render_template = 'news/form.html'

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(NewsPlugin)
