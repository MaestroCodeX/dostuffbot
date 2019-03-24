from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

import env
from src import logger


def start(bot, update):
    update.message.reply_text(
        (
            'Hello, my name is <b>Dostuffbot</b>!\n'
            'I am a bot for creating and hosting your bots.\n'
            'I can answer for specific commands that you teach me and send posts to users.\n\n'
            '<i>Bot commands:</i>\n'
            '/newbot\n'
            '/mybots\n\n'
            '<i>Extra commands:</i>\n'
            '/help\n'
            '/about\n'
            '/support\n'
        ),
        parse_mode=ParseMode.HTML,
    )


def main():
    updater = Updater(env.TOKEN)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)

    dp.add_handler(start_handler)
    dp.add_error_handler(logger.error)
    updater.start_polling()
    print('Bot is running.')
    updater.idle()


if __name__ == '__main__':
    main()
