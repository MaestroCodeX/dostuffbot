import logging

from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler

from src import secret

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

EMAIL = 1


def start(bot, update):
    update.message.reply_text('We are still working on it. Send email to get a notification when it\'s ready.')
    return EMAIL


def email(bot, update):
    msg = update.message
    bot.send_message(chat_id=secret.ADMIN_ID, text=f'{msg.from_user.id} {msg.from_user.first_name}- {msg.text}')
    update.message.reply_text('Thanks!')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(secret.TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={EMAIL: [RegexHandler(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)]},
        fallbacks=[],
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    print('Bot is running.')
    updater.idle()


if __name__ == '__main__':
    main()
