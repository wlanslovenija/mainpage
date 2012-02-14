def set_schema_search_path(sender, **kwargs):
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('SET search_path TO wlansi_cms, wlansi_nw')

from django.db.backends.signals import connection_created
connection_created.connect(set_schema_search_path)
