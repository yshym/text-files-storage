from .base import *


DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'textfilesstorage',
        'USER': 'textsuser',
        'PASSWORD': '123321',
        'HOST': 'localhost',
    }
}
