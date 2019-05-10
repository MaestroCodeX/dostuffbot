from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, Filters

from core.enums import DeepCommand
from core.utils import get_reply_function
from member import keyboards
from member.handlers import commands
from member.middleware import middleware
from member.utils import admin_only

START_MENU = range(1)


@admin_only
@middleware
def start(update, context):
    ''' Callback function when user sends /start or returns to main menu.
    It also handles start command with arguments from main bot. '''
    if update.message:
        args = update.message.text.split()[1:]
        if args:
            handle_deeplink(context.bot, update, args)
            # break further execution as soon as user did't want to send start command
            return

    reply_func = get_reply_function(update)
    if not reply_func:
        return

    reply_func(
        'Choose an option from the list below:',
        reply_markup=keyboards.start_markup(),
        parse_mode='MARKDOWN',
    )

    return START_MENU


def handle_deeplink(bot, update, args):
    command = args[0]

    if command == DeepCommand.COMMANDS:
        commands.commands_list(bot, update)


command_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^Commands$'), commands.commands_list)],
    states={
        1: [
            MessageHandler(Filters.command, commands.command_menu),
        ],
    },
    fallbacks=[],
)


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        START_MENU: [
            command_handler,
        ],
    },
    fallbacks=[],
)
