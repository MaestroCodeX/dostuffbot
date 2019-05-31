from telegram.ext import Dispatcher
from django.conf import settings

from member import texts, keyboards, states
from member.handlers import commands
from member.middleware import middleware


@middleware
def command_delete(update, context):
    """ Handle delete button in command menu.
    Do not delete the command but send confirmation request. """

    command = context.chat_data['cmd_instance']
    text = texts.delete_command(command)
    markup = keyboards.confirm_deletion_markup()
    update.message.reply_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')
    return states.DELETE_CONFIRM


@middleware
def command_delete_confirm(update, context):
    """ Handle delete confirmation button.
    Delete the command and return user to commands list. """

    command = context.chat_data['cmd_instance']
    dp = Dispatcher.get_instance()
    handlers = dp.handlers[settings.DEFAULT_HANDLER_GROUP]
    for h in handlers:
        if getattr(h, 'id', None) == command.id:
            dp.remove_handler(h, settings.DEFAULT_HANDLER_GROUP)
    command.delete()

    update.message.reply_text('The command has disappeared...')
    return commands.commands_list(update, context)
