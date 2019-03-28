
from telegram.ext import Filters, Updater, CommandHandler, ConversationHandler, MessageHandler

import env
from accounts import handlers as accounts_handlers
from bots import handlers as bots_handlers
from main import logger, handlers as main_handlers


def main():
    # Configure bot
    updater = Updater(env.TOKEN)
    dp = updater.dispatcher

    # Set handlers
    start_handler = CommandHandler('start', bots_handlers.start)
    new_bot_handler = ConversationHandler(
        entry_points=[CommandHandler('newbot', accounts_handlers.new_bot)],
        states={
            1: [MessageHandler(Filters.text, accounts_handlers.new_bot_token)]
        },
        fallbacks=[CommandHandler('cancel', bots_handlers.start)],
    )
    unknown_handler = MessageHandler(Filters.all, main_handlers.unknown)

    # Add handlers
    dp.add_handler(start_handler)
    dp.add_handler(new_bot_handler)
    dp.add_handler(unknown_handler)
    dp.add_error_handler(logger.error)

    # Start bot
    updater.start_polling()
    print('Bot is running.')
    updater.idle()
