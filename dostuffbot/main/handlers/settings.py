from telegram import ParseMode
from telegram.ext import CallbackQueryHandler

from main.models import User
from main.keyboards import settings_markup


def settings(bot, update):
    ''' Settings with inline keyboard '''
    query = update.callback_query

    user = User.objects.get(id=query.from_user.id)
    text = '***Language***: ' + user.lang
    query.edit_message_text(text=text, reply_markup=settings_markup, parse_mode=ParseMode.MARKDOWN)


settings_handler = CallbackQueryHandler(settings, pattern='settings')
