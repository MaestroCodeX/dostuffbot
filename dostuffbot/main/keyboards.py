from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from main.utils import e, get_deeplink, call_bot


start_kb = [
    [InlineKeyboardButton(e('Connect my bot :pushpin:'), callback_data='connect_bot')],
    [InlineKeyboardButton(e('My bots :closed_book:'), callback_data='my_bots')],
    [
        InlineKeyboardButton('Settings ⚙️', callback_data='settings'),
        InlineKeyboardButton(e('Help :question:'), callback_data='help'),
        InlineKeyboardButton(e('About me :pencil2:'), callback_data='about'),
    ]
]
cancel_start_kb = [[
    InlineKeyboardButton(e('Cancel :x:'), callback_data='start'),
]]
settings_kb = [[
    InlineKeyboardButton('Edit Language', callback_data='edit_lang'),
    InlineKeyboardButton('Back to menu', callback_data='start'),
]]
help_kb = [[
    InlineKeyboardButton('FAQs', callback_data='faq'),
    InlineKeyboardButton('Back to menu', callback_data='start'),
]]
about_kb = [
    [
        InlineKeyboardButton('Donate', callback_data='donate'),
        InlineKeyboardButton('Contact me', url='https://t.me/dostuffsupportbot'),
    ],
    [InlineKeyboardButton('Back to menu', callback_data='start')],
]

start_markup = InlineKeyboardMarkup(start_kb)
cancel_start_markup = InlineKeyboardMarkup(cancel_start_kb)
settings_markup = InlineKeyboardMarkup(settings_kb)
help_markup = InlineKeyboardMarkup(help_kb)
about_markup = InlineKeyboardMarkup(about_kb)


def get_profile_markup(bot):
    profile_kb = [
        [
            InlineKeyboardButton('Manage commands', url=get_deeplink(bot.name, 'commands')),
            InlineKeyboardButton('Notify bot users', url=get_deeplink(bot.name, 'notify')),
        ],
        [
            InlineKeyboardButton('Settings', callback_data=call_bot(bot.id, 'settings')),
            InlineKeyboardButton('Delete bot', callback_data=call_bot(bot.id, 'delete')),
        ],
        [InlineKeyboardButton('Back to menu', callback_data='start')],
    ]

    return InlineKeyboardMarkup(profile_kb)
