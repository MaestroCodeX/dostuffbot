import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from main.utils import e, build_deeplink, call_bot

BACK_TO_MENU_BTN = InlineKeyboardButton('« Back to menu', callback_data='start')
CONNECT_BOT_BTN = InlineKeyboardButton(e('Connect my bot :heavy_plus_sign:'), callback_data='connect_bot')

START_KB = [
    [CONNECT_BOT_BTN],
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
    BACK_TO_MENU_BTN,
]]
HELP_KB = [[
    InlineKeyboardButton('FAQs', callback_data='faq'),
    BACK_TO_MENU_BTN,
]]
ABOUT_KB = [
    [
        InlineKeyboardButton('Donate', callback_data='donate'),
        InlineKeyboardButton('Contact me', url='https://t.me/dostuffsupportbot'),
    ],
    [BACK_TO_MENU_BTN],
]
DONATE_KB = [
    [
        InlineKeyboardButton(f'{n}$', callback_data=f'donate__{n}')
        for n in [1, 2, 5, 10, 50, 100]
    ],
    [
        InlineKeyboardButton('Custom', callback_data='donate_custom'),
        InlineKeyboardButton('« Back to about', callback_data='about'),
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
        InlineKeyboardButton('« Back', callback_data='donate'),
    ],
]
CONNECT_BOT_KB = [[
    CONNECT_BOT_BTN, BACK_TO_MENU_BTN,
]]

START_M = InlineKeyboardMarkup(START_KB)
CANCEL_START_M = InlineKeyboardMarkup(CANCEL_START_KB)
SETTINGS_M = InlineKeyboardMarkup(SETTINGS_KB)
HTLP_M = InlineKeyboardMarkup(HELP_KB)
ABOUT_M = InlineKeyboardMarkup(ABOUT_KB)
DONATE_M = InlineKeyboardMarkup(DONATE_KB)
DONATE_CUSTOM_M = InlineKeyboardMarkup(DONATE_CUSTOM_KB)
CONNECT_BOT_M = InlineKeyboardMarkup(CONNECT_BOT_KB)


def bot_profile_m(bot):
    keyboard = [
        [
            InlineKeyboardButton('Manage commands', url=build_deeplink(bot.username, 'commands')),
            InlineKeyboardButton('Notify bot users', url=build_deeplink(bot.username, 'notify')),
        ],
        [
            InlineKeyboardButton('Settings', callback_data=call_bot(bot.id, 'settings')),
            InlineKeyboardButton('Delete bot', callback_data=call_bot(bot.id, 'delete')),
        ],
        [InlineKeyboardButton('« Back to bots list', callback_data='my_bots')],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_bot_button(bot):
    return InlineKeyboardButton(bot.full_username, callback_data=call_bot(bot.id, 'profile'))


def my_bots_m(bots):
    keyboard = []
    iter_bots = iter(bots)

    keyboard = [
        [
            get_bot_button(right),
            get_bot_button(left),
        ]
        for left, right in zip(iter_bots, iter_bots)
    ]

    # Add last bot, if the number of bots is odd
    if bots.count() % 2 == 1:
        keyboard.append(
            [get_bot_button(bots.last())]
        )

    keyboard.append([BACK_TO_MENU_BTN])
    return InlineKeyboardMarkup(keyboard)


def confirm_deletion_markup(bot):
    keyboard = [
        [InlineKeyboardButton('No', callback_data=call_bot(bot.id, 'profile'))],
        [InlineKeyboardButton('Nope, nevermind', callback_data=call_bot(bot.id, 'profile'))],
        [InlineKeyboardButton('Yes, delete the bot', callback_data=call_bot(bot.id, 'delete_confirm'))],
    ]
    random.shuffle(keyboard)
    back_to_bot_btn = InlineKeyboardButton('« Back to bots list', callback_data=call_bot(bot.id, 'profile'))
    keyboard.append([back_to_bot_btn])

    return InlineKeyboardMarkup(keyboard)
