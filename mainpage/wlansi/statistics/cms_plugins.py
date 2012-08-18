from django.db import models as django_models
from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from frontend.nodes import models

class StatisticsPlugin(plugin_base.CMSPluginBase):
    """
    This plugin outputs nodewatcher global statistics.
    """

    module = 'wlan slovenija'
    name = _("Statistics")
    render_template = 'statistics/statistics.html'

    def render(self, context, instance, placeholder):
        context.update({
            'nodes_count': models.Node.objects.exclude(node_type__in=(models.NodeType.Test, models.NodeType.Dead)).filter(status=models.NodeStatus.Up).count(),
            'clients_online' : models.APClient.objects.all().count(),
            'clients_ever' : models.Node.objects.aggregate(num=django_models.Sum('clients_so_far'))['num'] or 0,
        })

        return context

plugin_pool.register_plugin(StatisticsPlugin)
