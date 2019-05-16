from telegram.ext import Dispatcher
from django.conf import settings

from core.enums import CommandStatus
from member import texts, keyboards, states
from member.middleware import middleware
from member.models import Command


@middleware
def commands_list(update, context):
    """ Callback function to show all commands. """

    commands = Command.objects.filter(bot=context.bot.db_bot, status=CommandStatus.DONE)
    text = 'This is a list of your commands. Select command to see the details:'
    if not commands:
        text = 'Press "Add command" to create your first command.'

    update.message.reply_text(
        text,
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )

    return states.COMMAND_MENU


@middleware
def command_menu(update, context):
    """ Callback function to show command menu that was chosen from the list. """

    caller = update.message.text
    command = Command.objects.get(caller=caller)
    update.message.reply_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(),
        parse_mode='MARKDOWN',
    )

    context.chat_data['cmd_instance'] = command
    return states.CHOOSE_COMMAND_OPTION


@middleware
def command_delete(update, context):
    """ Handle delete button in command menu.
    Do not delete the command but send confirmation request. """

    command = context.chat_data['cmd_instance']
    text = texts.delete_command(command)
    markup = keyboards.confirm_deletion_markup(command)

    update.message.reply_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')

    return states.DELETE_CONFIRM


@middleware
def command_delete_confirm(update, context):
    """ Handle delete confirmation button.
    Delete the command and return user to commands list. """

    command = context.chat_data['cmd_instance']
    dp = Dispatcher.get_instance()
    handlers = dp.handlers[settings.DEFAULT_HANDLER_GROUP]
    for handler in handlers:
        print(handler.filters)
    command.delete()

    update.message.reply_text('The command has disappeared...')
    commands_list(update, context)


@middleware
def command_delete_decline(update, context):
    """ Handle delete dcline button.
    Don't delete the command and return user to command menu. """
    pass


@middleware
def command_show_answer(update, context):
    command = context.chat_data['cmd_instance']
    command.reply_to(update.message)

    update.message.reply_text(
        'The full answer is shown. Select what you want to do next:',
        reply_markup=keyboards.command_shown_markup()
    )
