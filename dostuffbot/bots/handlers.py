from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, CommandHandler, CallbackQueryHandler, MessageHandler

from accounts.models import User
from accounts.utils import get_user_from_message
from bots.models import Bot


def start_cmd(bot, update):
    """ The start was called with /start """
    message = update.message
    user = get_user_from_message(message)
    keyboard = [
        [InlineKeyboardButton('Add bot', callback_data='add_bot')],
        [InlineKeyboardButton('My bots', callback_data='my_bots')],
        [
            InlineKeyboardButton('Settings', callback_data='settings'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    sent_message = message.reply_text(
        '***Dostuffbot*** is here!\nPlease select what you want to do.',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup,
    )

    user.update_dialog(bot, sent_message.message_id)
    message.delete()


def start(bot, update):
    """ The start was called with callback """
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton('Add bot', callback_data='add_bot')],
        [InlineKeyboardButton('My bots', callback_data='my_bots')],
        [
            InlineKeyboardButton('Settings', callback_data='settings'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text(
        '***Dostuffbot*** is here!\nPlease select what you want to do.',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup,
    )


def add_bot(bot, update):
    query = update.callback_query
    keyboard = [[
        InlineKeyboardButton('Cancel', callback_data='start'),
    ]]
    markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text(
        'Send me please your bot token.\nYou can find it with @BotFather.',
        reply_markup=markup,
    )

    return 1


def token(bot, update):
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


def my_bots(bot, update):
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


def unknown(bot, update):
    """ Default handler when no other handler worked. Just delete the message. """
    update.message.delete()


start_cmd_handler = CommandHandler('start', start_cmd)
start_handler = CallbackQueryHandler(start, pattern='start')
add_bot_handler = CallbackQueryHandler(add_bot, pattern='add_bot')
my_bots_handler = CallbackQueryHandler(my_bots, pattern='my_bots')
token_handler = MessageHandler(Filters.regex(r'\d*:.*'), token)
unknown_handler = MessageHandler(Filters.all, unknown)
