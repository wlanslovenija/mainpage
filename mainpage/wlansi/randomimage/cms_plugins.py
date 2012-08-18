from django.utils.translation import ugettext_lazy as _

from cms import models as cms_models, plugin_base
from cms.plugin_pool import plugin_pool

from filer.models import imagemodels

from cmsplugin_blog import models as blog_models

from cmsplugin_filer_folder import cms_plugins

class RandomImagePlugin(plugin_base.CMSPluginBase):
    """
    This plugin outputs a random image from images used in cmsplugin-filer folder plugin instances used in blog.
    """

    module = 'wlan slovenija'
    name = _("Random image")
    render_template = 'randomimage/randomimage.html'

    def render(self, context, instance, placeholder):
        blog_entries = blog_models.Entry.published.all()
        blog_placeholders = cms_models.Placeholder.objects.filter(entry__in=blog_entries)
        plugins = cms_models.CMSPlugin.objects.filter(placeholder__in=blog_placeholders, plugin_type=cms_plugins.FilerFolderPlugin.__name__)
        images = imagemodels.Image.objects.filter(folder__in=plugins.values('filerfolder__folder'))

        context.update({
            'object': instance,
            'placeholder': placeholder,
            'images': images.order_by('?')[:4],
        })

        return context

plugin_pool.register_plugin(RandomImagePlugin)
