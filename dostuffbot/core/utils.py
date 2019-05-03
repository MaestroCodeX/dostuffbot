import emoji

from telegram import InlineKeyboardButton


def back_button(section, callback_data=None):
    callback_data = callback_data or section
    return InlineKeyboardButton(
        f'« Back to {section}',
        callback_data=callback_data.replace(' ', '_'),
    )


def build_deeplink(bot_name: str, parametr: str = None) -> str:
    link = 'https://t.me/' + bot_name
    if parametr:
        link += '?start=' + parametr
    return link


def get_fullname(user):
    if user.username:
        return '@' + user.username
    fullname = user.first_name
    if user.last_name:
        fullname += ' ' + user.last_name
    return fullname


def emojize(text):
    return emoji.emojize(text, use_aliases=True)
