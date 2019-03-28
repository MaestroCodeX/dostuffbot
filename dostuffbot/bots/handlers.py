from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from accounts.utils import get_user_from_message


def start(bot, update):
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

    user.update_dialog(bot, sent_message)
    message.delete()
