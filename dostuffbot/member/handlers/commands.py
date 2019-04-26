from telegram.ext import CallbackQueryHandler

from member import texts, keyboards
from member.models import Command
from member.utils import call_command_regex, get_command_from_call


def commands_list(bot, update):
    query = update.callback_query
    commands = Command.objects.all()
    query.edit_message_text(
        texts.COMMANDS,
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )


def command_menu(bot, update):
    query = update.callback_query
    command = get_command_from_call(query.data)
    query.edit_message_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(command),
        parse_mode='MARKDOWN',
    )


commands_list_handler = CallbackQueryHandler(commands_list, pattern='commands_list')
command_menu_handler = CallbackQueryHandler(command_menu, pattern=call_command_regex('menu'))
