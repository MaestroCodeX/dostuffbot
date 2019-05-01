import re

from telegram.ext import CallbackQueryHandler

from member import texts, keyboards
from member.middleware import middleware
from member.models import Command
from member.utils import (
    call_command_regex,
    get_command_from_call,
    get_command_id_from_call,
)


@middleware
def commands_list(bot, update):
    query = update.callback_query
    commands = Command.objects.all()
    query.edit_message_text(
        'This is a list of your commands. Select command to see the details:',
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )


@middleware
def command_add(bot, update):
    query = update.callback_query

    text = (
        'Now send a command that you want to add.\n\n'
        'Here are some examples:\n'
        '/start\n/help\n/about\\_project\n/chapter\\_3'
    )
    query.edit_message_text(
        text,
        reply_markup=keyboards.back_markup('commands list'),
        parse_mode='MARKDOWN',
    )


def command_add_caller(bot, update):
    caller = update.message.text
    if not re.match(r'^\/\w+$', caller):
        update.message.reply_text(
            'The command should start with / and can only contain [a-Z] letters, [0-9] numbers and "\\_"',
        )


@middleware
def command_menu(bot, update):
    query = update.callback_query
    command = get_command_from_call(query.data)
    query.edit_message_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(command),
        parse_mode='MARKDOWN',
    )


@middleware
def command_delete(bot, update):
    '''
    Handle delete button in command menu.
    Do not delete the command but send confirmation request.
    '''
    query = update.callback_query

    command = get_command_from_call(query.data)
    text = texts.delete_command(command)
    markup = keyboards.confirm_deletion_markup(command)

    query.edit_message_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')


@middleware
def command_edit(bot, update):
    query = update.callback_query

    command_id = get_command_id_from_call(query.data)
    query.edit_message_text(
        text='What do you want to edit?',
        reply_markup=keyboards.command_edit_markup(command_id),
        parse_mode='MARKDOWN',
    )


@middleware
def command_edit_command(bot, update):
    query = update.callback_query

    command_id = get_command_id_from_call(query.data)
    query.edit_message_text(
        text='What do you want to edit?',
        reply_markup=keyboards.command_edit_markup(command_id),
        parse_mode='MARKDOWN',
    )


@middleware
def command_delete_confirm(bot, update):
    '''
    Handle delete confirmation button.
    Delete the command and return user to commands list.
    '''
    query = update.callback_query

    command = get_command_from_call(query.data)
    command.delete()

    query.answer('The command has disappeared...')
    commands_list(bot, update)


commands_list_handler = CallbackQueryHandler(commands_list, pattern='commands_list')
command_add_handler = CallbackQueryHandler(command_add, pattern='command_add')
command_menu_handler = CallbackQueryHandler(command_menu, pattern=call_command_regex('menu'))
command_delete_handler = CallbackQueryHandler(command_delete, pattern=call_command_regex('delete'))
command_delete_confirm_handler = CallbackQueryHandler(
    command_delete_confirm,
    pattern=call_command_regex('delete_confirm'),
)
command_edit_handlers = CallbackQueryHandler(command_edit, pattern=call_command_regex('edit'))
