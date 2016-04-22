import urllib

from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

MAP_LATITUDE = '46.15'
MAP_LONGITUDE = '14.97'
MAP_ZOOM = 8

# TODO: Provide a search box next to the map so users can search for a location faster
# TODO: We should remember map position in the URL anchor

class MapPlugin(plugin_base.CMSPluginBase):
    """
    This plugin outputs dynamic Google Maps map of the network.
    """

    module = 'wlan slovenija'
    name = _("Map")
    render_template = 'map/map.html'

    def render(self, context, instance, placeholder):

        context.update({
            'MAP_LATITUDE': MAP_LATITUDE,
            'MAP_LONGITUDE': MAP_LONGITUDE,
            'MAP_ZOOM': MAP_ZOOM,
        })

        return context

plugin_pool.register_plugin(MapPlugin)
