from telegram.ext import CallbackQueryHandler

from member import texts, keyboards
from member.middleware import middleware
from member.models import Command
from member.utils import call_command_regex, get_command_from_call


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
command_menu_handler = CallbackQueryHandler(command_menu, pattern=call_command_regex('menu'))
command_delete_handler = CallbackQueryHandler(command_delete, pattern=call_command_regex('delete'))
command_delete_confirm_handler = CallbackQueryHandler(
    command_delete_confirm,
    pattern=call_command_regex('delete_confirm'),
)
