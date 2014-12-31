from .base import *


SECRET_KEY = 'h*&xek^=4o@y(r!kckn!ng1*si4g^*v$2+mz!6043*_j41*ycs'

DEBUG = True
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEV_APPS = (
)

DEV_MIDDLEWARE = (
)

INSTALLED_APPS += DEV_APPS
MIDDLEWARE_CLASSES = DEV_MIDDLEWARE + MIDDLEWARE_CLASSES
