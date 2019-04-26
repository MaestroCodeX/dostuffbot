from telegram import InlineKeyboardButton


def back_button(section, callback_data=None):
    return InlineKeyboardButton(
        f'« Back to {section}',
        callback_data=callback_data or section.replace(' ', '_'),
    )


def build_deeplink(bot_name: str, parametr: str = None) -> str:
    link = 'https://t.me/' + bot_name
    if parametr:
        link += '?start=' + parametr
    return link
