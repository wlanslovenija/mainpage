from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def render_gallery(context, plugin):
    try:
        return plugin.render_plugin(context, context['placeholder'])
    except:
        if settings.TEMPLATE_DEBUG:
            raise
        else:
            return u''
