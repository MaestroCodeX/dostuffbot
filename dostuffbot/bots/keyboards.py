from telegram import InlineKeyboardButton, InlineKeyboardMarkup


start_kb = [
    [InlineKeyboardButton('Add bot', callback_data='add_bot')],
    [InlineKeyboardButton('My bots', callback_data='my_bots')],
    [
        InlineKeyboardButton('Settings', callback_data='settings'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
    ]
]
cancel_start_kb = [[
    InlineKeyboardButton('Cancel', callback_data='start'),
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
