from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from main.utils import e, get_deeplink, call_bot


START_KB = [
    [InlineKeyboardButton(e('Connect my bot :pushpin:'), callback_data='connect_bot')],
    [InlineKeyboardButton(e('My bots :closed_book:'), callback_data='my_bots')],
    [
        InlineKeyboardButton('Settings ⚙️', callback_data='settings'),
        InlineKeyboardButton(e('Help :question:'), callback_data='help'),
        InlineKeyboardButton(e('About me :pencil2:'), callback_data='about'),
    ]
]
CANCEL_START_KB = [[
    InlineKeyboardButton(e('Cancel :x:'), callback_data='start'),
]]
SETTINGS_KB = [[
    InlineKeyboardButton('Edit Language', callback_data='edit_lang'),
    InlineKeyboardButton('Back to menu', callback_data='start'),
]]
HELP_KB = [[
    InlineKeyboardButton('FAQs', callback_data='faq'),
    InlineKeyboardButton('Back to menu', callback_data='start'),
]]
ABOUT_KB = [
    [
        InlineKeyboardButton('Donate', callback_data='donate'),
        InlineKeyboardButton('Contact me', url='https://t.me/dostuffsupportbot'),
    ],
    [InlineKeyboardButton('Back to menu', callback_data='start')],
]
DONATE_KB = [
    [
        InlineKeyboardButton(f'{n}$', callback_data=f'donate_{n}')
        for n in [1, 2, 5, 10, 50, 100]
    ],
    [
        InlineKeyboardButton('Custom', callback_data='donate_custom'),
        InlineKeyboardButton('Back to menu', callback_data='about'),
    ],
]
DONATE_CUSTOM_KB = [
    *[
        [
            InlineKeyboardButton(str(x*3+y+1), callback_data=f'donate_add__{x*3+y+1}')
            for y in range(3)
        ]
        for x in range(3)
    ],
    [
        InlineKeyboardButton(' ', callback_data=' '),
        InlineKeyboardButton('0', callback_data='donate_add__0'),
        InlineKeyboardButton('<', callback_data='donate_erase'),
    ],
    [
        InlineKeyboardButton('Submit', callback_data='donate_submit'),
        InlineKeyboardButton('Back', callback_data='donate'),
    ],
]

START_M = InlineKeyboardMarkup(START_KB)
CANCEL_START_M = InlineKeyboardMarkup(CANCEL_START_KB)
SETTINGS_M = InlineKeyboardMarkup(SETTINGS_KB)
HTLP_M = InlineKeyboardMarkup(HELP_KB)
ABOUT_M = InlineKeyboardMarkup(ABOUT_KB)
DONATE_M = InlineKeyboardMarkup(DONATE_KB)
DONATE_CUSTOM_M = InlineKeyboardMarkup(DONATE_CUSTOM_KB)


def profile_m(bot):
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
