from telegram.ext import CallbackQueryHandler, CommandHandler

from core.enums import DeepCommand
from core.utils import get_reply_function
from member import keyboards
from member.handlers import commands
from member.middleware import middleware
from member.utils import admin_only


@admin_only
@middleware
def start(bot, update):
    if update.message:
        args = update.message.text.split()[1:]
        if args:
            handle_deeplink(bot, update, args)
            # break further execution as soon as user did't want to send start command
            return

    reply_func = get_reply_function(update)
    if not reply_func:
        return

    reply_func(
        'Choose an option from the list below:',
        reply_markup=keyboards.start_markup(bot.db_bot),
        parse_mode='MARKDOWN',
    )


def handle_deeplink(bot, update, args):
    command = args[0]

    if command == DeepCommand.COMMANDS:
        commands.commands_list(bot, update)


start_command_handler = CommandHandler('start', start)
start_handler = CallbackQueryHandler(start, pattern='start')
