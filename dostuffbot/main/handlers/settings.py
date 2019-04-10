from telegram.ext import CallbackQueryHandler

from main import keyboards
from main.models import User


def settings(bot, update):
    ''' Settings with inline keyboard '''
    query = update.callback_query

    user = User.objects.get(id=query.from_user.id)
    text = '***Language***: ' + user.lang
    query.edit_message_text(text=text, reply_markup=keyboards.SETTINGS_M, parse_mode='MARKDOWN')


settings_handler = CallbackQueryHandler(settings, pattern='settings')
