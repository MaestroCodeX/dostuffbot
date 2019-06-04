import random

from telegram import ReplyKeyboardMarkup

from member import texts


def to_keyboard(schema):
    return ReplyKeyboardMarkup(schema, resize_keyboard=True)


def start_markup():
    schema = [
        [texts.COMMANDS],
        [texts.SEND_NOTIFICATION],
        [texts.SETTINGS, texts.HELP],
    ]
    return to_keyboard(schema)


def commands_markup(commands):
    schema = [
        *[[c.caller] for c in commands],
        [texts.ADD_COMMAND,
            texts.back_text('start')],
    ]
    return to_keyboard(schema)


def command_menu_markup():
    schema = [
        [texts.EDIT_COMMAND],
        [texts.EDIT_ANSWER],
        [texts.SHOW_ANSWER],
        [
            texts.DELETE_COMMAND,
            texts.back_text('commands list'),
        ]
    ]
    return to_keyboard(schema)


def confirm_deletion_markup():
    schema = [
        ['No'],
        ['Nope, nevermind'],
        [texts.DELETE_COMMAND_CONFIRM],
    ]
    random.shuffle(schema)
    schema.append([texts.back_text('command menu')])

    return to_keyboard(schema)


def command_shown_markup():
    schema = [[
        texts.EDIT_ANSWER,
        texts.back_text('command menu'),
    ]]
    return to_keyboard(schema)


def command_adding_markup():
    schema = [[
        texts.COMPLETE,
        texts.CANCEL,
    ]]
    return to_keyboard(schema)


def cancel_markup():
    schema = [[
        texts.CANCEL
    ]]
    return to_keyboard(schema)


def edit_asnwer_markup():
    schema = [
        [texts.DELETE_ALL_MESSAGES],
        [texts.DELETE_LAST_MESSAGE],
        [
            texts.UNDO_LAST,
            texts.back_text('menu'),
        ],
    ]
    return to_keyboard(schema)


def back_markup(section):
    schema = [[texts.back_text(section)]]
    return to_keyboard(schema)


def confirm_yes_no_markup():
    schema = [[texts.YES, texts.NO]]
    return to_keyboard(schema)
