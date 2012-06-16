from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': (
        'django.conf',
        'mainpage.wlansi',
    ),
}

urlpatterns = patterns('',
    url(r'^admin/cms/plugin/markup/', include('cmsplugin_markup.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/js/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^', include('cms.urls')),
    url(r'^', include('filer.server.urls')),
)

# For development, serve static files through Django
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns()
