import posixpath

from django.utils.translation import ugettext_lazy as _

from cms import plugin_base

from filer.fields import image

import cmsplugin_filer_utils

class HoverAnimation(plugin_base.CMSPlugin):
    static_image = image.FilerImageField(verbose_name=_("static image"), related_name='hoveranimation_staticimage_set')
    animation = image.FilerImageField(verbose_name=_("animation"), related_name='hoveranimation_animation_set')

    objects = cmsplugin_filer_utils.FilerPluginManager(select_related=('static_image', 'animation'))

    def __unicode__(self):
        if self.static_image:
            return posixpath.basename(self.static_image.path)
        elif self.animation:
            return posixpath.basename(self.animation.path)
        return "<empty>"
