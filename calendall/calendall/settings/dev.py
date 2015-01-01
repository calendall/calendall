import os

from .base import *


SECRET_KEY = 'h*&xek^=4o@y(r!kckn!ng1*si4g^*v$2+mz!6043*_j41*ycs'

DEBUG = True
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'calendall',
        'USER': 'calendall',
        'PASSWORD': 'calendall',
        # This settings are related with Docker, postgresql is a host
        # (see fig.yml) that points to the postgresql container, we could use
        # os.getenv('POSTGRESQL_PORT_5432_TCP_ADDR', 'localhost'),
        'HOST': 'postgresql',
        'PORT': os.getenv('POSTGRESQL_PORT_5432_TCP_PORT', '5432'),
    }
}

DEV_APPS = (
)

DEV_MIDDLEWARE = (
)

INSTALLED_APPS += DEV_APPS
MIDDLEWARE_CLASSES = DEV_MIDDLEWARE + MIDDLEWARE_CLASSES
