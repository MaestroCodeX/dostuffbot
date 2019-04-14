from telegram.ext import CommandHandler

from member import texts, keyboards


def start(bot, update):
    ''' The start was called with /start '''
    update.message.reply_text(
        texts.START,
        reply_markup=keyboards.START_M,
        parse_mode='MARKDOWN',
    )


start_handler = CommandHandler('start', start)
