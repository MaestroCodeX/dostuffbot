import logging

from telegram.ext import Updater

import env
from core import logger


def main():
    # Configure bot
    updater = Updater(env.MEMBER_TOKEN)
    dp = updater.dispatcher

    # Add handlers

    # Log all errors
    dp.add_error_handler(logger.error)

    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
    updater.idle()
