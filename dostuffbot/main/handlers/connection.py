from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, CallbackQueryHandler, MessageHandler

from main.models import User, Bot
from main.keyboards import cancel_start_markup
from main.texts import add_bot_text


def add_bot(bot, update):
    ''' Connect bot handler method called with inline keyboard '''
    query = update.callback_query

    query.answer()
    query.edit_message_text(add_bot_text, reply_markup=cancel_start_markup)

    return 1


def token(bot, update):
    ''' Add bot with sent token '''
    user = User.objects.get(id=update.message.from_user.id)
    token = update.message.text

    Bot.objects.create(owner=user, token=token, name='@Name')

    keyboard = [[
        InlineKeyboardButton('Menu', callback_data='start'),
    ]]
    markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=user.id,
        message_id=user.dialog_id,
        text='Your bot was succesfully added to the system!',
        reply_markup=markup,
    )

    update.message.delete()


add_bot_handler = CallbackQueryHandler(add_bot, pattern='add_bot')
token_handler = MessageHandler(Filters.regex(r'\d*:.*'), token)
