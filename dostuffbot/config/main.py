import logging

from telegram.ext import Updater

import env
from main.handlers import (
    connection,
    maintance,
    management,
    start,
    settings,
    support,
)
from config import logger


def main():
    # Configure bot
    updater = Updater(env.TOKEN)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(start.start_cmd_handler)
    dp.add_handler(start.start_handler)
    dp.add_handler(connection.add_bot_handler)
    dp.add_handler(connection.token_handler)
    dp.add_handler(management.my_bots_handler)
    dp.add_handler(settings.settings_handler)
    dp.add_handler(support.help_handler)
    dp.add_handler(support.about_handler)
    dp.add_handler(maintance.unknown_handler)

    # Log all errors
    dp.add_error_handler(logger.error)

    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
    updater.idle()
