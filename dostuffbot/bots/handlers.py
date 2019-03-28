from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from accounts.utils import get_user_from_message


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
    )
    query.edit_message_reply_markup(reply_markup=markup)


def add_bot(bot, update):
    query = update.callback_query
    keyboard = [[
        InlineKeyboardButton('Cancel', callback_data='start'),
    ]]
    markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text('Send me please your bot token.\nYou can find it with @BotFather.')
    query.edit_message_reply_markup(reply_markup=markup)

    return 1
