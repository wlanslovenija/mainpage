def set_schema_search_path(sender, **kwargs):
    from django.conf import settings
    from django.db import connection

    path = ','.join((settings.DATABASES['default']['USER'], settings.DATABASES['users']['USER']))

    cursor = connection.cursor()
    cursor.execute('SET search_path TO %s' % (path,))

from django.db.backends.signals import connection_created
connection_created.connect(set_schema_search_path)

class UserModelRouter(object):
    """
	A router to route all operations on `django.contrib.auth.models.User` objects to ``users`` database.
	"""

    def db_for_read(self, model, **hints):
        if model._meta.db_table == 'auth_user':
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == 'auth_user':
            return 'users'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table == 'auth_user' or obj2._meta.db_table == 'auth_user':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'users':
            return model._meta.db_table == 'auth_user'
        elif model._meta.db_table == 'auth_user':
            return False
        return None
