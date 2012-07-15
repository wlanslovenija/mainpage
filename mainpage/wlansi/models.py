from django.conf import settings
from django.db.backends.signals import connection_created

def set_schema_search_path(sender, **kwargs):
    from django.db import connection, transaction
    
    cursor = connection.cursor()
    cursor.execute('SET search_path TO %s' % ', '.join(settings.DATABASES['default']['SCHEMA_SEARCH_PATH']))
    transaction.commit_unless_managed()

if 'postgresql' in settings.DATABASES['default']['ENGINE'] and settings.DATABASES['default'].get('SCHEMA_SEARCH_PATH'):
    connection_created.connect(set_schema_search_path)
