import logging

from telegram.ext import Updater

import env
from core import logger
from main.handlers import (
    connection,
    maintance,
    management,
    start,
    settings,
    support,
)


def main():
    # Configure bot
    updater = Updater(env.TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(start.start_command_handler)
    dp.add_handler(start.start_handler)
    dp.add_handler(connection.connect_bot_handler)
    dp.add_handler(management.my_bots_handler)
    dp.add_handler(management.bot_profile_handler)
    dp.add_handler(management.bot_settings_handler)
    dp.add_handler(management.delete_bot_handler)
    dp.add_handler(management.delete_bot_confirm_handler)
    dp.add_handler(settings.settings_handler)
    dp.add_handler(settings.edit_lang_handler)
    dp.add_handler(settings.lang_list_handler)
    dp.add_handler(support.help_handler)
    dp.add_handler(support.about_handler)
    dp.add_handler(support.faq_handler)
    dp.add_handler(support.faq_by_id_handler)
    dp.add_handler(support.faq_rate_handler)
    dp.add_handler(support.donate_handler)
    dp.add_handler(support.donate_predefined_handler)
    dp.add_handler(support.donate_custom_handler)
    dp.add_handler(support.donate_add_handler)
    dp.add_handler(support.donate_erase_handler)
    dp.add_handler(support.donate_submit_handler)
    dp.add_handler(maintance.unknown_handler)

    # Log all errors
    dp.add_error_handler(logger.error)

    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
    updater.idle()


if __name__ == '__main__':
    main()
