from django.conf import settings
from django.core import urlresolvers
from django.utils import translation

class ForceAdminLanguage(object):
    def process_request(self, request):
        admin_url = urlresolvers.reverse('admin:index')
        admin_preview_url = admin_url + 'r/'
        if request.path.startswith(admin_url) and not request.path.startswith(admin_preview_url):
            translation.activate(settings.ADMIN_LANGUAGE_CODE)

        return None
