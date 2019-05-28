from django.conf import settings
from telegram.ext import CallbackQueryHandler

from main import keyboards, texts
from main.models import User


def my_settings(update, context, user=None):
    """ Settings with inline keyboard """
    query = update.callback_query

    user = user or User.objects.get(id=query.from_user.id)

    query.edit_message_text(text=texts.settings(user), reply_markup=keyboards.SETTINGS_M, parse_mode='MARKDOWN')


def lang_list(update, context):
    """ Send available languages list to user to change language interface. """
    query = update.callback_query

    query.edit_message_text(text=texts.EDIT_LANG, reply_markup=keyboards.EDIT_LANG_M, parse_mode='MARKDOWN')


def edit_lang(update, context):
    """ Edit language interface with selected one from list. """
    query = update.callback_query

    user = User.objects.get(id=query.from_user.id)
    lang = query.data.split('__')[1]\

    supported_languages = dict(settings.LANGUAGES)
    if lang in supported_languages:
        user.lang = lang
        user.save()

    my_settings(update, context, user)


settings_handler = CallbackQueryHandler(my_settings, pattern='settings')
lang_list_handler = CallbackQueryHandler(lang_list, pattern='lang_list')
edit_lang_handler = CallbackQueryHandler(edit_lang, pattern='edit_lang__.*')
