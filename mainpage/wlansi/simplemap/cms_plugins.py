import urllib

from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from frontend.nodes import models

SIMPLEMAP_WIDTH = 298
SIMPLEMAP_HEIGHT = 200
MARKER_URL = 'http://bit.ly/RpSQDF'

class SimpleMapPlugin(plugin_base.CMSPluginBase):
    """
    This plugin outputs static Google Maps map of the network.
    """

    module = 'wlan slovenija'
    name = _("Simple map")
    render_template = 'simplemap/simplemap.html'

    def render(self, context, instance, placeholder):
        nodes = models.Node.objects.exclude(node_type__in=(models.NodeType.Test, models.NodeType.Dead)).exclude(geo_lat__isnull=True).exclude(geo_long__isnull=True).filter(status=models.NodeStatus.Up)
        # There is a 2048 character limit to HTTP GET request URL length, so we round locations to one decimal and display them only once
        # TODO: We could count how many nodes fall into the same location and use different (max 5) markers of intensity (like heatmap)
        markers = set(['%(geo_lat).1f,%(geo_long).1f' % node for node in nodes.values('geo_lat', 'geo_long')])

        parameters = {
            'center': '46.15,14.97',
            'zoom': 7,
            'size': '%dx%d' % (SIMPLEMAP_WIDTH, SIMPLEMAP_HEIGHT),
            'sensor': 'false',
            'style': ('feature:road|visibility:off', 'element:labels|visibility:off', 'feature:all|hue:0x1072b1|gamma:3'),
            'markers': '|'.join(['shadow:false', 'icon:%s' % MARKER_URL] + list(markers)),
        }

        context.update({
            'parameters': urllib.urlencode(parameters, doseq=True),
            'width': SIMPLEMAP_WIDTH,
            'height': SIMPLEMAP_HEIGHT,
        })

        return context

plugin_pool.register_plugin(SimpleMapPlugin)
