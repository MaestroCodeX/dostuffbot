import logging

from telegram.ext import Updater, Filters, MessageHandler

from core import logger
from member import constants
from member.handlers import start, commands, notifications

ADMIN_GROUP = 1
ADMIN_HANDLERS = [
    start.start_handler,
    start.menu_handler,
    commands.commands_handler,
    notifications.notify_handler,
]


def get_handler(command):
    def handler(bot, update):
        update.message.reply_text(
            command.content,
            parse_mode='MARKDOWN',
        )

    return handler


def command_handler(command):
    return MessageHandler(Filters.regex(command.text), get_handler(command))


def run_bot_with_handlers(instance):
    # Configure bot
    updater = Updater(instance.token)
    dp = updater.dispatcher
    constants.BOT_ID = instance.id

    # Add handlers
    for handler in ADMIN_HANDLERS:
        dp.add_handler(handler, group=ADMIN_GROUP)

    commands = instance.commands.all()
    for command in commands:
        handler = command_handler(command)
        dp.add_handler(handler)

    # Log all errors
    dp.add_error_handler(logger.error)

    # TODO: Run bot in a new thread
    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
