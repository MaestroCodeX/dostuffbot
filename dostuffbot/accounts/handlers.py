# TODO: This is one time solution to work database models.
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()


from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from accounts.models import User
from bots.models import Bot


def new_bot_token(bot, update):
    message = update.message
    user = User.objects.get(id=message.from_user.id)
    token = message.text
    Bot.objects.create(owner=user, token=token)

    keyboard = [[
        InlineKeyboardButton('Cancel', callback_data='start'),
    ]]
    markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=user.id,
        message_id=user.dialog_id,
        text='Your bot was succesfully added to the system!',
        reply_markup=markup,
    )

    message.delete()
    return ConversationHandler.END
