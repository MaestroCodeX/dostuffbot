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
    'main',
    'member',
)

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('ru', _('Russian')),
)
LANGUAGE_CODE = 'en'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

SECRET_KEY = env.SECRET_KEY
BOT_CALL_PREFIX = 'bot_'
BOT_ID_REGEX = BOT_CALL_PREFIX + r'(\d*)__.*'
COMMAND_CALL_PREFIX = 'command_'
COMMAND_ID_REGEX = COMMAND_CALL_PREFIX + r'(\d*)__.*'
DEFAULT_HANDLER_GROUP = 0
MAX_MEMBER_COMMANDS = 10
