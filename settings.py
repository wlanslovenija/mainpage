# -*- coding: utf-8 -*-
# Django settings for mainpage project.

# Secrets are in a separate file so they are not visible in public repository
from secrets import *

import os

_ = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'webmaster@biolab.si'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'db.sqlite',
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'biolab',                                   # Or path to database file if using sqlite3.
        'USER': 'django',                                   # Not used with sqlite3.
        'PASSWORD': '',                                     # Not used with sqlite3.
        'HOST': '',                                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                         # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
)

URL_VALIDATOR_USER_AGENT = 'Django'

# Date input formats below take as first argument day and then month in x/y/z format
DATE_INPUT_FORMATS = (
    '%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y', '%b %d %Y',
    '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
    '%B %d, %Y', '%d %B %Y', '%d %B, %Y',
)

# All those formats are only defaults and are localized for users
DATE_FORMAT = 'd/M/Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'd/M/Y, H:i'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'j F'
SHORT_DATE_FORMAT = 'd/m/y'
SHORT_DATETIME_FORMAT = 'd/m/y H:i'
FIRST_DAY_OF_WEEK = 1
DECIMAL_SEPARATOR = '.'
THOUSAND_SEPARATOR = ','
NUMBER_GROUPING = 0

# We override defaults
FORMAT_MODULE_PATH = 'formats'

LOGIN_REDIRECT_URL = '/admin/'
LOGIN_URL = '/admin/'
LOGOUT_URL = '/admin/'

FORCE_SCRIPT_NAME = ''

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = MEDIA_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# SECRET_KEY is in secrets

DEFAULT_FROM_EMAIL = 'webmaster@biolab.si'
EMAIL_SUBJECT_PREFIX = '[Orange] '

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    #'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'mainpage.urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "templates"),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'cms',
    'mptt',
    'menus',
    'south',
    'appmedia',
    'easy_thumbnails',
    'filer',
    'tagging',
    'reversion',
    'djangocms_utils',
    'simple_translation',
    'cmsplugin_blog',
    'cms.plugins.link',
    'cms.plugins.snippet',
    #'cms.plugins.inherit',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    'cmsplugin_filer_image',
    'cmsplugin_markup',
    'missing',
)

CMS_TEMPLATES = (
    ('main.html', 'Main Page'),
    ('blog.html', 'Blog Page'),
)

# Not really used as we are not using django-cms core plugins for files but django-filer
#CMS_PAGE_MEDIA_PATH = 'assets/'

CMS_USE_TINYMCE = False

CMS_MARKUP_OPTIONS = (
    'cmsplugin_markup_tracwiki',
)

CMS_MARKUP_TRAC_INTERTRAC = {
    'trac': {
        'TITLE': 'Orange Trac',
        'URL': 'http://orange.biolab.si/trac',
    },
}

CMS_URL_OVERWRITE = False
CMS_MENU_TITLE_OVERWRITE = False
CMS_REDIRECTS = False
CMS_FLAT_URLS = False
CMS_SOFTROOT = True

CMS_PERMISSION = False
CMS_MODERATOR = False
CMS_SHOW_START_DATE = True
CMS_SHOW_END_DATE = True
CMS_SEO_FIELDS = False
PLACEHOLDER_FRONTEND_EDITING = False

CMSPLUGIN_BLOG_PLACEHOLDERS = ('on_index_page', 'the_rest')

JQUERY_UI_CSS = os.path.join(MEDIA_URL, "jquery", "jquery-ui.min.css")
JQUERY_JS = os.path.join(MEDIA_URL, "jquery", "jquery.min.js")
JQUERY_UI_JS = os.path.join(MEDIA_URL, "jquery", "jquery-ui.min.js")

THUMBNAIL_DEBUG = False
THUMBNAIL_QUALITY = 95
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

VIDEO_FULLSCREEN = False

FILER_PAGINATE_BY = 50
FILER_SUBJECT_LOCATION_IMAGE_DEBUG = False
FILER_IS_PUBLIC_DEFAULT = True
FILER_PUBLICMEDIA_ROOT = os.path.join(MEDIA_ROOT, 'files')
FILER_PUBLICMEDIA_URL = os.path.join(MEDIA_URL, 'files/')
FILER_PUBLICMEDIA_THUMBNAIL_ROOT = os.path.join(MEDIA_ROOT, 'thumbnails')
FILER_PUBLICMEDIA_THUMBNAIL_URL = os.path.join(MEDIA_URL, 'thumbnails/')
FILER_PRIVATEMEDIA_ROOT = os.path.abspath(os.path.join(MEDIA_ROOT, '..', 'smedia', 'files'))
FILER_PRIVATEMEDIA_URL = '/smedia/files/'
FILER_PRIVATEMEDIA_THUMBNAIL_ROOT = os.path.abspath(os.path.join(MEDIA_ROOT, '..', 'smedia', 'thumbnails'))
FILER_PRIVATEMEDIA_THUMBNAIL_URL = '/smedia/thumbnails/'
FILER_IMAGE_USE_ICON = True

if not DEBUG:
    from filer.server.backends.xsendfile import ApacheXSendfileServer

    FILER_PRIVATEMEDIA_SERVER = ApacheXSendfileServer()
    FILER_PRIVATEMEDIA_THUMBNAIL_SERVER = ApacheXSendfileServer()
