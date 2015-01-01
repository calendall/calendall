from .base import *


SECRET_KEY = '^7$+=8rj(utk59qe_5j%+sn0jzc^&)zxua04aik8+@t0-yjoj2'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'ubuntu',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432
    }
}
