# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .settings import *

# Secrets are in a separate file so they are not visible in public repository
from .secrets import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Webmaster', 'webmaster@wlan-si.net'),
)

MANAGERS = ADMINS

# We set search path to include nodewatcher's schema, so we can share some
# tables (like users) between them. The idea is that we delete users table from
# mainpage's schema so that it is found in nodewatcher's schema.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wlansi',
        'USER': 'wlansi_cms',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
        'SCHEMA_SEARCH_PATH': ('wlansi_cms', 'wlansi_nw'),
    },
}

# SECRET_KEY is in secrets

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# RECAPTCHA_PUBLIC_KEY is in secrets
# RECAPTCHA_PRIVATE_KEY is in secrets

GIT_REPOSITORIES_DIR = '/srv/git/'

if DEBUG:
    # So that headers and template contexts are populated with debug data
    INTERNAL_IPS = AllIPs()
else:
    INTERNAL_IPS = ()

from filer.storage import PublicFileSystemStorage, PrivateFileSystemStorage

FILER_PUBLICMEDIA_STORAGE = PublicFileSystemStorage(
    location=FILER_PUBLICMEDIA_ROOT,
    base_url=FILER_PUBLICMEDIA_URL
)
FILER_PUBLICMEDIA_THUMBNAIL_STORAGE = PublicFileSystemStorage(
    location=FILER_PUBLICMEDIA_THUMBNAIL_ROOT,
    base_url=FILER_PUBLICMEDIA_THUMBNAIL_URL
)
FILER_PRIVATEMEDIA_STORAGE = PrivateFileSystemStorage(
    location=FILER_PRIVATEMEDIA_ROOT,
    base_url=FILER_PRIVATEMEDIA_URL
)
FILER_PRIVATEMEDIA_THUMBNAIL_STORAGE = PrivateFileSystemStorage(
    location=FILER_PRIVATEMEDIA_THUMBNAIL_ROOT,
    base_url=FILER_PRIVATEMEDIA_THUMBNAIL_URL
)

if not DEBUG:
    from filer.server.backends.nginx import NginxXAccelRedirectServer

    FILER_PRIVATEMEDIA_SERVER = NginxXAccelRedirectServer(
        location=FILER_PRIVATEMEDIA_ROOT,
        nginx_location='/nginx_filer_private_files'
    )
    FILER_PRIVATEMEDIA_THUMBNAIL_SERVER = NginxXAccelRedirectServer(
        location=FILER_PRIVATEMEDIA_THUMBNAIL_ROOT,
        nginx_location='/nginx_filer_private_thumbnails'
    )
