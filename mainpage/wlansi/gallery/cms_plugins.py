from django.utils.translation import ugettext_lazy as _

from cms import models as cms_models, plugin_base
from cms.plugin_pool import plugin_pool

from cmsplugin_blog import models as blog_models

from cmsplugin_filer_folder import cms_plugins

class GalleryPlugin(plugin_base.CMSPluginBase):
    """
    This plugin outputs gallery built from all used cmsplugin-filer folder plugin instances used in blog.
    """

    module = 'wlan slovenija'
    name = _("Gallery")
    render_template = 'gallery/gallery.html'

    def render(self, context, instance, placeholder):
        blog_entries = blog_models.Entry.published.all()
        blog_placeholders = cms_models.Placeholder.objects.filter(entry__in=blog_entries)
        plugins = cms_models.CMSPlugin.objects.filter(placeholder__in=blog_placeholders, plugin_type=cms_plugins.FilerFolderPlugin.__name__).order_by('-placeholder__entry__pub_date')

        seen_folders = set()

        def distinct_plugins():
            for plugin in plugins:
                instance = plugin.get_plugin_instance()[0]

                if instance is None:
                    # Invalid plugin instance, we ignore it
                    continue

                if instance.folder not in seen_folders:
                    seen_folders.add(instance.folder)
                    yield (plugin, instance)

        context.update({
            'object': instance,
            'placeholder': placeholder,
            'plugins': distinct_plugins(),
        })

        return context

plugin_pool.register_plugin(GalleryPlugin)
