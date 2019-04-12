from telegram.ext import CallbackQueryHandler

from main import keyboards, texts
from main.models import User


def my_settings(bot, update):
    ''' Settings with inline keyboard '''
    query = update.callback_query

    user = User.objects.get(id=query.from_user.id)
    text = '***Language***: ' + user.lang
    query.edit_message_text(text=text, reply_markup=keyboards.SETTINGS_M, parse_mode='MARKDOWN')


def edit_lang(bot, update):
    ''' Send available languages list to user to change language interface. '''
    query = update.callback_query

    query.edit_message_text(text=texts.EDIT_LANG, reply_markup=keyboards.EDIT_LANG_M, parse_mode='MARKDOWN')


settings_handler = CallbackQueryHandler(my_settings, pattern='settings')
edit_lang_handler = CallbackQueryHandler(edit_lang, pattern='edit_lang')
