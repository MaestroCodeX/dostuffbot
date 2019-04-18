from telegram.ext import Filters, CommandHandler, MessageHandler

from member import texts, keyboards
from member.handlers import commands, notifications
from member.utils import admin_only


@admin_only
def start(bot, update):
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
