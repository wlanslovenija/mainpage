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

AUTHENTICATION_BACKENDS += (
    'frontend.account.auth.AprBackend',
    'frontend.account.auth.CryptBackend',
)

# RECAPTCHA_PUBLIC_KEY is in secrets
# RECAPTCHA_PRIVATE_KEY is in secrets

CMS_MARKUP_TRAC_COMPONENTS += (
    'tracdashessyntax.plugin.DashesSyntaxPlugin',
    'footnotemacro.macro.FootNoteMacro',
    'mathjax.api.MathJaxPlugin',
    'tracmath.tracmath.TracMathPlugin',
)

if DEBUG:
    # So that headers and template contexts are populated with debug data
    INTERNAL_IPS = AllIPs()
else:
    INTERNAL_IPS = ()

FILER_STORAGES['public']['main']['ENGINE'] = 'filer.storage.PublicFileSystemStorage'
FILER_STORAGES['public']['thumbnails']['ENGINE'] = 'filer.storage.PublicFileSystemStorage'
FILER_STORAGES['private']['main']['ENGINE'] = 'filer.storage.PrivateFileSystemStorage'
FILER_STORAGES['private']['thumbnails']['ENGINE'] = 'filer.storage.PrivateFileSystemStorage'

# TODO: Enable when Nginx backend will properly set MIME
if False and not DEBUG:
    FILER_SERVERS = {
        'private': {
            'main': {
                'ENGINE': 'filer.server.backends.nginx.NginxXAccelRedirectServer',
                'OPTIONS': {
                    'location': FILER_PRIVATEMEDIA_ROOT,
                    'nginx_location': '/nginx_filer_private_files',
                },
            },
            'thumbnails': {
                'ENGINE': 'filer.server.backends.nginx.NginxXAccelRedirectServer',
                'OPTIONS': {
                    'location': FILER_PRIVATEMEDIA_THUMBNAIL_ROOT,
                    'nginx_location': '/nginx_filer_private_thumbnails',
                },
            },
        },
    }

GIT_REPOSITORIES_DIR = '/srv/git/'
