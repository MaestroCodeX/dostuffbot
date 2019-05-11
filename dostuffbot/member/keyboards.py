import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

import env
from core.enums import CommandMessageType
from core.utils import back_button, build_deeplink
from main.utils import call_bot
from member.utils import call_command


def to_keyboard(schema):
    keyboard = [
        [KeyboardButton(text) for text in row]
        for row in schema
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def start_markup():
    schema = [
        ['Commands'],
        ['Send notification'],
        ['Settings'],
    ]
    return to_keyboard(schema)


def commands_markup(commands):
    schema = [
        *[[c.caller] for c in commands],
        ['Add command'],
        ['Back to start'],
    ]
    return to_keyboard(schema)


def command_menu_markup():
    schema = [
        ['Edit command'],
        ['Edit answer'],
        ['Show answer'],
        ['Delete command', 'Back to commands list']
    ]
    return to_keyboard(schema)


def confirm_deletion_markup(command):
    keyboard = [
        ['No'],
        ['Nope, nevermind'],
        ['Yes, delete the command'],
    ]
    random.shuffle(keyboard)
    keyboard.append(['Back to command menu.'])

    return to_keyboard(schema)


def command_shown_markup(command):
    keyboard = [[
            InlineKeyboardButton('Edit answer', callback_data=call_command(command.id, 'edit_answer')),
            back_button('command menu', call_command(command.id, 'menu')),
    ]]
    return InlineKeyboardMarkup(keyboard)


def back_markup(caption, data=None):
    keyboard = [[back_button(caption, data or caption)]]
    return InlineKeyboardMarkup(keyboard)


def back_command_menu_markup(command_id):
    return back_markup('command menu', call_command(command_id, 'menu'))
