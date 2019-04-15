import logging

from telegram.ext import Updater

from core import logger
from member import constants
from member.handlers import start


DEFAULT_HANDLERS = [
    start.start_handler,
]


def run_bot_with_handlers(instance):
    # Configure bot
    updater = Updater(instance.token)
    dp = updater.dispatcher
    constants.BOT_ID = instance.id

    # Add handlers
    for handler in DEFAULT_HANDLERS:
        dp.add_handler(handler)

    # Log all errors
    dp.add_error_handler(logger.error)

    # TODO: Run bot in a new thread
    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
    updater.idle()
