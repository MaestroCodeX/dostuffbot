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


def get_telegram_user_from_update(update):
    if update.effective_user:
        return update.effective_user
    elif update.channel_post:
        return update.channel_post.from_user


def get_fullname(user):
    if user.username:
        return '@' + user.username
    fullname = user.first_name
    if user.last_name:
        fullname += ' ' + user.last_name
    return fullname


def get_reply_function(update):
    if update.callback_query:
        return update.callback_query.edit_message_text
    elif update.message:
        return update.message.reply_text


def emojize(text):
    return emoji.emojize(text, use_aliases=True)
