from telegram import KeyboardButton, ReplyKeyboardMarkup


START_KB = [[
    KeyboardButton('Commands'),
    KeyboardButton('Send notification'),
    KeyboardButton('Scheduled notification'),
]]


START_M = ReplyKeyboardMarkup(START_KB, resize_keyboard=True)
