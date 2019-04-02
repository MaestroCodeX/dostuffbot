import logging

from telegram.ext import Updater

import env
from internal import handlers as internal_handlers
from config import logger


def main():
    # Configure bot
    updater = Updater(env.TOKEN)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(internal_handlers.start_cmd_handler)
    dp.add_handler(internal_handlers.start_handler)
    dp.add_handler(internal_handlers.add_bot_handler)
    dp.add_handler(internal_handlers.my_bots_handler)
    dp.add_handler(internal_handlers.token_handler)
    dp.add_handler(internal_handlers.settings_handler)
    dp.add_handler(internal_handlers.help_handler)
    dp.add_handler(internal_handlers.about_handler)
    dp.add_handler(internal_handlers.smile_admin_handler)
    dp.add_handler(internal_handlers.smile_again_handler)
    dp.add_handler(internal_handlers.unknown_handler)

    # Log all errors
    dp.add_error_handler(logger.error)

    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
    updater.idle()
