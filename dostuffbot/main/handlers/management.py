from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from main.models import User


def my_bots(bot, update):
    ''' Show my bots with inline keyboard '''
    query = update.callback_query
    user = User.objects.get(id=query.from_user.id)
    bots = user.bot_set.all()

    keyboard = []
    iter_bots = iter(bots)
    for left, right in zip(iter_bots, iter_bots):
        row = [
            InlineKeyboardButton(left.name, callback_data='bot_detail' + str(left.id)),
            InlineKeyboardButton(right.name, callback_data='bot_detail' + str(right.id)),
        ]
        keyboard.append(row)

    if bots.count() % 2 == 1:
        # Add last bot, if the count is odd
        last = bots.last()
        row = [
            InlineKeyboardButton(last.name, callback_data='bot_detail' + str(last.id)),
        ]
        keyboard.append(row)

    text = 'Choose a bot from list:'
    if not bots.count():
        text = 'You don\'t have bots yet.'
        add_bot_kb = [InlineKeyboardButton('Add bot', callback_data='add_bot')]
        keyboard.append(add_bot_kb)

    cancel_kb = [InlineKeyboardButton('Cancel', callback_data='start')]
    keyboard.append(cancel_kb)

    markup = InlineKeyboardMarkup(keyboard)
    query.answer()
    query.edit_message_text(text=text, reply_markup=markup)


my_bots_handler = CallbackQueryHandler(my_bots, pattern='my_bots')
