from .base import *


DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'textfilesstorage',
        'USER': 'postgres',
        'HOST': 'localhost',
    }
}
