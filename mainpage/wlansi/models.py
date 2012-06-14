"""
Set search path to include nodewatcher's schema, so we
can share some tables (like users) between them.

This only works with PostgreSQL.
"""

def set_schema_search_path(sender, **kwargs):
    from django.db import connection
    
    cursor = connection.cursor()
    cursor.execute('SET search_path TO wlansi_cms, wlansi_nw')

from django.conf import settings
from django.db.backends.signals import connection_created

if 'postgresql' in settings.DATABASES['default']['ENGINE']:
    connection_created.connect(set_schema_search_path)
