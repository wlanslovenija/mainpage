def set_schema_search_path(sender, **kwargs):
    from django.conf import settings
    from django.db import connection
    
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        cursor = connection.cursor()
        cursor.execute('SET search_path TO wlansi_cms, wlansi_nw')

from django.db.backends.signals import connection_created
connection_created.connect(set_schema_search_path)
