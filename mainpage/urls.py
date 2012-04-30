from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/cms/plugin/markup/', include('cmsplugin_markup.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('cms.urls')),
    (r'^', include('filer.server.urls')),
)

if getattr(settings, 'DEBUG', None):
    # Serve static files with Django when running in debug mode
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns
