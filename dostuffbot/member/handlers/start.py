from telegram.ext import Filters, CommandHandler, MessageHandler

from member import texts, keyboards
from member.constants import BOT_ID
from member.handlers import commands, notifications
from member.models import Subscriber
from member.utils import admin_only, get_me_from_db


@admin_only
def start(bot, update):
    my_bot = get_me_from_db(bot)
    Subscriber.objects.get_or_create(id=update.effective_user.id, bot=my_bot)
    args = update.message.text.split()
    if args[0] == '/start' and len(args) > 1:
        argument = args[0]
        if argument == 'commands':
            commands.commands(bot, update)
            return

        if argument == 'notify':
            notifications.notify_claim(bot, update)
            return

    update.message.reply_text(
        texts.START,
        reply_markup=keyboards.START_M,
        parse_mode='MARKDOWN',
    )


start_handler = CommandHandler('start', start)
menu_handler = MessageHandler(Filters.regex('Menu'), start)
