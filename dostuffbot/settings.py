import os
import env

from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'config',
    'main',
)

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)

SECRET_KEY = env.SECRET_KEY
