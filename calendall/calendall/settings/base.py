"""
Django settings for calendall project.
"""

# ------------- Helper stuff -------------
import os
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

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

PIPELINE_CSS = {
}

PIPELINE_JS = {
    'base-libs': {
        'source_filenames': (
            'bower/jquery/dist/jquery.js',
        ),
        'output_filename': 'js/base-libs.min.js',
    }
}

# ------------- User stuff -------------
AUTH_USER_MODEL = 'profiles.CalendallUser'

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
