from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher

from core.enums import DeepCommand
from member import texts, keyboards
from member.handlers import commands
from member.utils import admin_only, middleware


@admin_only
@middleware
def start_command(bot, update):
    dispatcher = Dispatcher.get_instance()
    db_bot = dispatcher.db_bot

    # args = update.message.text.split()
    # if len(args) > 1:
    #     handle_start_command(bot, update, args[1])
    #     # break further execution as soon as user did't want to send start command
    #     return

    update.message.reply_text(
        texts.START,
        reply_markup=keyboards.start_markup(db_bot),
        parse_mode='MARKDOWN',
    )


def start(bot, update):
    query = update.callback_query
    dispatcher = Dispatcher.get_instance()
    db_bot = dispatcher.db_bot

    query.edit_message_text(
        texts.START,
        reply_markup=keyboards.start_markup(db_bot),
        parse_mode='MARKDOWN',
    )


def handle_start_command(bot, update, command):
    if command == DeepCommand.COMMANDS:
        commands.commands(bot, update)
    elif command == DeepCommand.NOTIFY:
        update.message.text = 'Send notification'
        Dispatcher.get_instance().process_update(update)


start_command_handler = CommandHandler('start', start_command)
start_handler = CallbackQueryHandler(start, pattern='start')
