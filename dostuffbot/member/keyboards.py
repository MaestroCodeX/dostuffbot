from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import env
from core.utils import back_button, build_deeplink
from main.utils import call_bot
from member.utils import call_command


def commands_markup(commands):
    keyboard = [
        [InlineKeyboardButton(c.command, callback_data=call_command(c.id, 'menu'))]
        for c in commands
    ]
    keyboard.append([InlineKeyboardButton('Menu', callback_data='start')])
    keyboard.append([InlineKeyboardButton('Add command', callback_data='command_add')])
    return InlineKeyboardMarkup(keyboard)


def command_menu_markup(command):
    keyboard = [
        [InlineKeyboardButton('Edit command', callback_data=call_command(command.id, 'edit'))],
        [InlineKeyboardButton('See answer', callback_data=call_command(command.id, 'full_answer'))],
        [InlineKeyboardButton('Delete command', callback_data=call_command(command.id, 'delete'))],
        [back_button('commands list')],
    ]
    return InlineKeyboardMarkup(keyboard)


def start_markup(bot):
    keyboard = [
        [InlineKeyboardButton('Commands', callback_data='commands_list')],
        [InlineKeyboardButton('Send notification', callback_data='notify')],
        [InlineKeyboardButton('Settings', url=build_deeplink(env.BOT_USERNAME, call_bot(bot.id, 'settings')))],
    ]

    return InlineKeyboardMarkup(keyboard)


CANCEL_KB = [[
    InlineKeyboardButton('Cancel'),
]]

CANCEL_M = InlineKeyboardMarkup(CANCEL_KB)
