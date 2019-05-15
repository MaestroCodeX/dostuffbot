import logging

from telegram.ext import Updater
from django.conf import settings

from core import logger
from member.states import base_conversation
from member.utils import get_command_handler

ADMIN_HANDLERS = [
    base_conversation,
]


def run_bot_with_handlers(instance):
    # Configure bot
    # my_persistence = PicklePersistence(filename='my_file')
    updater = Updater(instance.token, use_context=True)
    dp = updater.dispatcher
    dp.db_bot = instance
    dp.bot.db_bot = instance

    # Add handlers
    for handler in ADMIN_HANDLERS:
        dp.add_handler(handler, group=settings.ADMIN_HANDLER_GROUP)

    commands = instance.commands.all()
    for command in commands:
        handler = get_command_handler(command)
        dp.add_handler(handler, group=settings.DEFAULT_HANDLER_GROUP)

    # Log all errors
    dp.add_error_handler(logger.error)

    # TODO: Run bot in a new thread
    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
