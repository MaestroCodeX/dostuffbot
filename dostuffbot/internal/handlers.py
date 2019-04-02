from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, CommandHandler, CallbackQueryHandler, MessageHandler

from internal.models import User, Bot
from internal.utils import get_user_from_message
from internal.keyboards import start_markup, cancel_start_markup, settings_markup, help_markup, about_markup
from internal.texts import start_text, add_bot_text, help_text, about_text


def start_cmd(bot, update):
    """ The start was called with /start """
    message = update.message
    user = get_user_from_message(message)

    sent_message = message.reply_text(start_text, parse_mode=ParseMode.MARKDOWN, reply_markup=start_markup)

    user.update_dialog(bot, sent_message.message_id)
    message.delete()


def start(bot, update):
    """ The start was called with inline keyboard """
    query = update.callback_query

    query.answer()
    query.edit_message_text(start_text, parse_mode=ParseMode.MARKDOWN, reply_markup=start_markup)


def add_bot(bot, update):
    """ Add bot with inline keyboard """
    query = update.callback_query

    query.answer()
    query.edit_message_text(add_bot_text, reply_markup=cancel_start_markup,)

    return 1


def token(bot, update):
    """ Add bot with sent token """
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
    """ Show my bots with inline keyboard """
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


def settings(bot, update):
    """ Settings with inline keyboard """
    query = update.callback_query

    user = User.objects.get(id=query.from_user.id)
    text = '***Language***: ' + user.lang
    query.edit_message_text(text=text, reply_markup=settings_markup, parse_mode=ParseMode.MARKDOWN)


def help(bot, update):
    """ Help section with inline keyboard """
    query = update.callback_query
    query.edit_message_text(text=help_text, reply_markup=help_markup, parse_mode=ParseMode.MARKDOWN)


def about(bot, update):
    """ About section with inline keyboard """
    query = update.callback_query
    query.edit_message_text(text=about_text, reply_markup=about_markup)


def unknown(bot, update):
    """ Default handler when no other handlers worked. Just delete the message. """
    update.message.delete()


start_cmd_handler = CommandHandler('start', start_cmd)

start_handler = CallbackQueryHandler(start, pattern='start')
add_bot_handler = CallbackQueryHandler(add_bot, pattern='add_bot')
my_bots_handler = CallbackQueryHandler(my_bots, pattern='my_bots')
settings_handler = CallbackQueryHandler(settings, pattern='settings')
help_handler = CallbackQueryHandler(help, pattern='help')
about_handler = CallbackQueryHandler(about, pattern='about')
smile_admin_handler = CallbackQueryHandler(about, pattern='smile_admin')
smile_again_handler = CallbackQueryHandler(about, pattern='smile_again')

token_handler = MessageHandler(Filters.regex(r'\d*:.*'), token)
unknown_handler = MessageHandler(Filters.all, unknown)
