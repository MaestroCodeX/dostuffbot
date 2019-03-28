# TODO: This is one time solution to work database models.
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()


from telegram import ParseMode
from telegram.ext import ConversationHandler

from accounts.models import Bot
from accounts.utils import get_user_from_message


def new_bot(bot, update):
    update.message.reply_text(
        'Send me please your Bot token. You can find it with @BotFather.',
        parse_mode=ParseMode.HTML,
    )

    return 1


def new_bot_token(bot, update):
    user = get_user_from_message(update.message)
    token = update.message.text
    Bot.objects.create(owner=user, token=token)
    update.message.reply_text('Your bot was succesfully added to the system!')

    return ConversationHandler.END
