import urllib

from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from frontend.nodes import models

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
        nodes = models.Node.objects.exclude(node_type__in=(models.NodeType.Test, models.NodeType.Dead)).exclude(geo_lat__isnull=True).exclude(geo_long__isnull=True).filter(status=models.NodeStatus.Up)

        for node in nodes:
            # TODO: Very ugly, but it works
            node.get_full_url = 'https://nodes.wlan-si.net/node/%s' % node.pk

        context.update({
            'nodes': nodes,
            'MAP_LATITUDE': MAP_LATITUDE,
            'MAP_LONGITUDE': MAP_LONGITUDE,
            'MAP_ZOOM': MAP_ZOOM,
        })

        return context

plugin_pool.register_plugin(MapPlugin)
