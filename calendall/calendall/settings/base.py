"""
Django settings for calendall project.
"""
import os

from django.core.urlresolvers import reverse_lazy
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# ------------- Helper stuff -------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# ------------- Security stuff -------------
SECRET_KEY = None
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = []

# ------------- Application stuff -------------
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'pipeline',
)

LOCAL_APPS = (
    'core',
    'profiles',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ------------- Middleware stuff -------------
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# ------------- Routing & server stuff -------------
ROOT_URLCONF = 'calendall.urls'
WSGI_APPLICATION = 'calendall.wsgi.application'
DOMAIN = "calendall.io"

# ------------- Database stuff -------------
DATABASES = None

# ------------- I18N & L10N stuff -------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ------------- Static & template stuff -------------
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

# FIX: This var will be deprecated
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

PIPELINE_CSS = {
    'base-libs': {
        'source_filenames': (
            'bower/semantic/dist/semantic.css',
        ),
        'output_filename': 'css/base-libs.min.css',
    },
    'email-libs': {
        'source_filenames': (
            "bower/transactional-email-templates/templates/styles.css",
        ),
        'output_filename': 'css/email-libs.min.css',
        # This shouldn't be compressed because we use premailer, for now use
        # like this
    }
}

PIPELINE_JS = {
    'base-libs': {
        'source_filenames': (
            'bower/jquery/dist/jquery.js',
            'bower/semantic/dist/semantic.js',
        ),
        'output_filename': 'js/base-libs.min.js',
    }
}

# ------------- Email Stuff -------------
EMAIL_BACKEND = None
EMAIL_SUPPORT = "support@calendall.com"
EMAIL_NOREPLY = "noreply@calendall.com"
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'me@gmail.com'
# EMAIL_HOST_PASSWORD = 'password'

# ------------- User stuff -------------
AUTH_USER_MODEL = 'profiles.CalendallUser'
LOGIN_URL = reverse_lazy("profiles:login")
LOGOUT_URL = reverse_lazy("profiles:logout")
LOGIN_REDIRECT_URL = reverse_lazy("profiles:login")

# ------------- Logging stuff -------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
            'log_colors': {
                'DEBUG':    'bold_cyan',
                'INFO':     'bold_green',
                'WARNING':  'bold_yellow',
                'ERROR':    'bold_red',
                'CRITICAL': 'bg_red',
            },
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'calendall.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        },
    },
    'loggers': {
        # Global handler
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        #'core': {
        #    'handlers': ['file', 'console'],
        #    'level': 'ERROR',
        #    'propagate': False,
        #},
    }
}
