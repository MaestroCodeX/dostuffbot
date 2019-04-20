from telegram import KeyboardButton, ReplyKeyboardMarkup


def commands_markup(commands):
    keyboard = [
        [KeyboardButton(c.command)]
        for c in commands
    ]
    keyboard.append([KeyboardButton('Menu')])
    keyboard.append([KeyboardButton('Add command')])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def command_menu_markup(command):
    keyboard = [
        [KeyboardButton('Edit command')],
        [KeyboardButton('See response')],
        [KeyboardButton('Delete command')],
        [KeyboardButton('Back to commands list')],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


START_KB = [[
    KeyboardButton('Commands'),
    KeyboardButton('Send notification'),
    KeyboardButton('Scheduled notification'),
]]


START_M = ReplyKeyboardMarkup(START_KB, resize_keyboard=True)
