from __future__ import absolute_import

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from . import models

class InMediaPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a list of publications about wlan slovenija in media and elsewhere.
    """

    module = 'wlan slovenija'
    name = _("In media")
    render_template = 'inmedia/list.html'

    def render(self, context, instance, placeholder):
        language = translation.get_language()
        context.update({
            'entries': models.InMediaEntry.objects.filter(descriptions__language=language),
        })
        return context

plugin_pool.register_plugin(InMediaPlugin)
