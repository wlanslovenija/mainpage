from __future__ import absolute_import

from django.conf import settings
from django.forms import widgets
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
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context

    def icon_src(self, instance):
        return settings.STATIC_URL + u"cms/images/plugins/snippet.png"

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'custom_css':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 60})
        return super(DummyPlugin, self).formfield_for_dbfield(db_field, **kwargs)

plugin_pool.register_plugin(DummyPlugin)
