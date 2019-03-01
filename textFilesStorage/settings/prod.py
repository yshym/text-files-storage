from .base import *


DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'textfilesstorage',
        'USER': 'textsuser',
        'PASSWORD': '123321',
        'HOST': 'localhost',
    }
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
