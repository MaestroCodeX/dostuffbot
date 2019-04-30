import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import env
from core.enums import CommandMessageType
from core.utils import back_button, build_deeplink
from main.utils import call_bot
from member.utils import call_command


def start_markup(bot):
    keyboard = [
        [InlineKeyboardButton('Commands', callback_data='commands_list')],
        [InlineKeyboardButton('Send notification', callback_data='notify')],
        [InlineKeyboardButton('Settings', url=build_deeplink(env.BOT_USERNAME, call_bot(bot.id, 'settings')))],
    ]

    return InlineKeyboardMarkup(keyboard)


def commands_markup(commands):
    keyboard = [
        [InlineKeyboardButton(c.command, callback_data=call_command(c.id, 'menu'))]
        for c in commands
    ]
    keyboard.append([
        InlineKeyboardButton('Add command', callback_data='command_add'),
        back_button('menu', 'start'),
    ])
    return InlineKeyboardMarkup(keyboard)


def command_menu_markup(command):
    keyboard = [
        [InlineKeyboardButton('Edit command', callback_data=call_command(command.id, 'edit'))],
    ]
    if command.command_messages.exclude(type=CommandMessageType.TEXT).exists():
        keyboard.append(
            [InlineKeyboardButton('See full answer', callback_data=call_command(command.id, 'full_answer'))]
        )

    keyboard.append(
        [
            InlineKeyboardButton('Delete command', callback_data=call_command(command.id, 'delete')),
            back_button('commands list')
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def confirm_deletion_markup(command):
    keyboard = [
        [InlineKeyboardButton('No', callback_data=call_command(command.id, 'menu'))],
        [InlineKeyboardButton('Nope, nevermind', callback_data=call_command(command.id, 'menu'))],
        [InlineKeyboardButton('Yes, delete the command', callback_data=call_command(command.id, 'delete_confirm'))],
    ]
    random.shuffle(keyboard)
    back_to_bot_btn = back_button('command menu', call_command(command.id, 'menu'))
    keyboard.append([back_to_bot_btn])

    return InlineKeyboardMarkup(keyboard)


def command_edit_markup(command_id):
    keyboard = [
        [
            InlineKeyboardButton('Edit command', callback_data=call_command(command_id, 'edit_text')),
            InlineKeyboardButton('Edit response', callback_data=call_command(command_id, 'edit_answer'))
        ],
        [back_button('command menu', call_command(command_id, 'menu'))],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_start():
    keyboard = [[back_button('menu', 'start')]]
    return InlineKeyboardMarkup(keyboard)
