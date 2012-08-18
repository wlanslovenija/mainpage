# -*- coding: utf-8 -*-

import os, sys

settings_dir = os.path.abspath(os.path.dirname(__file__))
database_file = os.path.join(settings_dir, 'db.sqlite')

# Website requires nodewatcher, so for easier development we assume
# it is accessible in the same directory website repository is
nodewatcher_dir = os.path.abspath(os.path.join(settings_dir, '..', '..', 'nodewatcher', 'nodewatcher'))
sys.path.insert(0, nodewatcher_dir)

# Dummy function, so that "makemessages" can find strings which should be translated.
_ = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# A tuple that lists people who get code error notifications. When
# DEBUG=False and a view raises an exception, Django will e-mail these
# people with the full exception information. Each member of the tuple
# should be a tuple of (Full name, e-mail address).
ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': database_file,                  # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    },
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
LANGUAGE_CODE = 'sl'

LANGUAGES = (
    ('sl', _('Slovenian')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(settings_dir, 'locale'),
)

ADMIN_LANGUAGE_CODE = 'en'

import frontend
GEOIP_PATH = os.path.abspath(os.path.join(os.path.dirname(frontend.__file__), '..', 'geoip'))
DEFAULT_COUNTRY = 'SI'

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
FORMAT_MODULE_PATH = 'mainpage.formats'

FORCE_SCRIPT_NAME = ''

AUTH_PROFILE_MODULE = 'account.UserProfileAndSettings'

SITE_ID = 3

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(settings_dir, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(settings_dir, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'u=@fy7qlo@e2ga1xv5=f(d1xx1$6bzj@em(9-5dhu)7as*#^5$'

EMAIL_HOST = 'localhost'
EMAIL_SUBJECT_PREFIX = '[wlan-si] '
DEFAULT_FROM_EMAIL = 'open@wlan-si.net'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
    'mainpage.wlansi.context_processors.global_vars',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'missing.middleware.ForceAdminLanguage',
    'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'mainpage.urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mainpage.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    # Here because of the weird import order problems with templates and sekizai
    'cmsplugin_markup_tracwiki',

    # Ours are first so that we can override default templates in other apps
    'frontend.account',
    'frontend.dns',
    'frontend.nodes',
    'mainpage.wlansi',
    'mainpage.wlansi.accounting',
    'mainpage.wlansi.donations',
    'mainpage.wlansi.dummy',
    'mainpage.wlansi.gallery',
    'mainpage.wlansi.inmedia',
    'mainpage.wlansi.news',
    'mainpage.wlansi.participants',
    'mainpage.wlansi.randomimage',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',

    'cms',
    'mptt',
    'menus',
    'south',
    'easy_thumbnails',
    'filer',
    'tagging',
    'reversion',
    'sekizai',
    'djangocms_utils',
    'simple_translation',
    'cmsplugin_blog',
    'cms.plugins.snippet',
    'cms.plugins.twitter',
    #'cms.plugins.inherit',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    'cmsplugin_filer_image',
    'cmsplugin_markup',
    'cmsplugin_contact',
    'missing',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/admin/'
LOGIN_URL = '/admin/'
LOGOUT_URL = '/admin/'

AUTHENTICATION_BACKENDS = (
    'frontend.account.auth.ModelBackend',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

FORCE_LOWERCASE_TAGS = True

CMS_TEMPLATES = (
    ('simple.html', 'Simple page'),
    ('simple_with_right.html', 'Page with right column'),
    ('simple_two_columns.html', 'Page with two columns'),
    ('layered_two_columns.html', 'Page with two columns, a header and a footer'),
    ('layered_three_columns.html', 'Page with three columns, a header and a footer'),
    ('main.html', 'Main page'),
    ('blog.html', 'Blog page'),
)

# Not really used as we are not using django-cms core plugins for files but django-filer
#CMS_PAGE_MEDIA_PATH = 'assets/'

CMS_USE_TINYMCE = False

CMS_MARKUP_OPTIONS = (
    'cmsplugin_markup_tracwiki',
)

CMS_MARKUP_TRAC_INTERTRAC = {
    'grow': {
        'TITLE': 'wlan slovenia growing',
        'URL': 'http://grow.wlan-si.net',
    },
    'interop': {
        'TITLE': 'Open Networks Interoperability',
        'URL': 'http://interop.wlan-si.net',
    },
    'dev': {
        'TITLE': 'wlan slovenia development',
        'URL': 'http://dev.wlan-si.net',
    },
}

CMS_MARKUP_TRAC_INTERWIKI = {
    'nodes': {
        'URL': 'https://nodes.wlan-si.net/',
    },
    'lists': {
        'URL': 'http://wlan-si.net/lists/arc/$1/$2-$3/msg$4.html',
    },
    'skypechat': {
        'URL': 'skype:?chat&blob=',
    },
    'wikipedia': {
        'URL': 'http://en.wikipedia.org/wiki/',
    },
    'slwikipedia': {
        'URL': 'http://sl.wikipedia.org/wiki/',
    },
}

CMS_MARKUP_TRAC_CONFIGURATION = {
    'tracmath': {
        'cache_dir': os.path.join(settings_dir, 'tracwiki', 'cache'),
    }
}

CMS_MARKUP_TRAC_TEMPLATES_DIR = os.path.join(settings_dir, 'tracwiki', 'templates')

CMS_MARKUP_TRAC_COMPONENTS = (
)

CMS_LANGUAGES_URL_IGNORE_PREFIXES = (
    '/lists',
    '/smedia/',
)

CMS_URL_OVERWRITE = False
CMS_MENU_TITLE_OVERWRITE = True
CMS_REDIRECTS = True
CMS_FLAT_URLS = True
CMS_SOFTROOT = False

CMS_PERMISSION = False
CMS_MODERATOR = False
CMS_SHOW_START_DATE = True
CMS_SHOW_END_DATE = True
CMS_SEO_FIELDS = False
PLACEHOLDER_FRONTEND_EDITING = False

CMSPLUGIN_BLOG_PLACEHOLDERS = ('on_index_page', 'the_rest')

JQUERY_JS = os.path.join(STATIC_URL, 'wlansi', 'jquery', 'jquery.min.js')
JQUERY_UI_CSS = os.path.join(STATIC_URL, 'wlansi', 'jquery', 'jquery-ui.min.css')
JQUERY_UI_JS = os.path.join(STATIC_URL, 'wlansi', 'jquery', 'jquery-ui.min.js')

THUMBNAIL_DEBUG = False
THUMBNAIL_QUALITY = 95
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

VIDEO_WIDTH = 480
VIDEO_HEIGHT = 360
VIDEO_FULLSCREEN = False

FILER_PAGINATE_BY = 50
FILER_SUBJECT_LOCATION_IMAGE_DEBUG = False
FILER_IS_PUBLIC_DEFAULT = True
FILER_IMAGE_USE_ICON = True
FILER_ENABLE_PERMISSIONS = True

class AllIPs(list):
    def __contains__(self, ip):
        return True

if DEBUG:
    # So that headers and template contexts are populated with debug data
    INTERNAL_IPS = AllIPs()

FILER_PUBLICMEDIA_ROOT = os.path.join(MEDIA_ROOT, 'files')
FILER_PUBLICMEDIA_URL = os.path.join(MEDIA_URL, 'files/')
FILER_PUBLICMEDIA_THUMBNAIL_ROOT = os.path.join(MEDIA_ROOT, 'thumbnails')
FILER_PUBLICMEDIA_THUMBNAIL_URL = os.path.join(MEDIA_URL, 'thumbnails/')
FILER_PRIVATEMEDIA_ROOT = os.path.abspath(os.path.join(MEDIA_ROOT, '..', 'smedia', 'files'))
FILER_PRIVATEMEDIA_URL = '/smedia/files/'
FILER_PRIVATEMEDIA_THUMBNAIL_ROOT = os.path.abspath(os.path.join(MEDIA_ROOT, '..', 'smedia', 'thumbnails'))
FILER_PRIVATEMEDIA_THUMBNAIL_URL = '/smedia/thumbnails/'

FILE_STORAGE_PREFIX = 'http://wlan-si.net'

FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'mainpage.wlansi.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': FILER_PUBLICMEDIA_ROOT,
                'base_url': FILER_PUBLICMEDIA_URL,
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
        },
        'thumbnails': {
            'ENGINE': 'mainpage.wlansi.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': FILER_PUBLICMEDIA_THUMBNAIL_ROOT,
                'base_url': FILER_PUBLICMEDIA_THUMBNAIL_URL,
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'mainpage.wlansi.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': FILER_PRIVATEMEDIA_ROOT,
                'base_url': FILER_PRIVATEMEDIA_URL,
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
        },
        'thumbnails': {
            'ENGINE': 'mainpage.wlansi.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': FILER_PRIVATEMEDIA_THUMBNAIL_ROOT,
                'base_url': FILER_PRIVATEMEDIA_THUMBNAIL_URL,
            },
        },
    },
}

CMSPLUGIN_FILER_FOLDER_VIEW_OPTIONS = (
    ('slideshow', 'Slideshow'),
    ('list', 'List'),
    ('supporters', 'Supporters'),
    ('panoramajs', 'Panoramas (JavaScript)'),
)

SUPPORTERS_FILER_FOLDER_NAME = 'Supporters'

GIT_REPOSITORIES_DIR = None
