from .base import *


DOMAIN = "ci.calendall.io"
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


# Don't execute migratiosn when testing
# http://stackoverflow.com/questions/25161425/disable-migrations-when-running-unit-tests-in-django-1-7
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()
