# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Webmaster', 'webmaster@wlan-si.net'),
)

MANAGERS = ADMINS

# We set search path to include nodewatcher's schema, so we can share some
# tables (like users) between them. The idea is that we delete users table from
# mainpage's schema so that it is found in nodewatcher's schema.

#DB_PASSWORD is defined in Dockerfile
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mainpage')

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

# SECRET_KEY is defined in Dockerfile
SECRET_KEY = os.environ.get('SECRET_KEY', 'ilikejimmyjams')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# We support some common password formats to ease transition
AUTHENTICATION_BACKENDS += (
    'frontend.account.auth.AprBackend',
    'frontend.account.auth.CryptBackend',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
}

# RECAPTCHA_PUBLIC_KEY is defined in Dockerfile
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
# RECAPTCHA_PRIVATE_KEY is defined in Dockerfile
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

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

if not DEBUG:
    PAYPAL_TEST = DEBUG
    PAYPAL_DEBUG = PAYPAL_TEST
    # PAYPAL_IDENTITY_TOKEN_PRODUCTION is defined in Dockerfile
    PAYPAL_IDENTITY_TOKEN = os.environ.get('PAYPAL_IDENTITY_TOKEN_PRODUCTION')
    PAYPAL_RECEIVER_EMAIL = 'mitar@tnode.com'
    PAYPAL_RECEIVER_EMAIL_ALIAS = 'order@wlan-si.net'
    PAYPAL_RECEIVER_EMAIL_DONATION_ALIAS = 'donate@wlan-si.net'
    PAYPAL_PRIVATE_CERT = os.path.join(paypal_dir, 'production.private')
    PAYPAL_PUBLIC_CERT = os.path.join(paypal_dir, 'production.public')
    PAYPAL_CERT = os.path.join(paypal_dir, 'paypal_production.pem')
    PAYPAL_CERT_ID = 'EWMRL6RHUA6NE'

USE_HTTPS = True
