from telegram.ext import Dispatcher, ConversationHandler, MessageHandler, Filters
from django.conf import settings

from core.enums import CommandStatus
from core.handlers import ignore
from member import texts, keyboards, states
from member.handlers import command_addition, start
from member.middleware import middleware
from member.models import Command
from member.utils import (
    to_filter_regex,
    back_to_message_handler
)


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

    return states.BACK


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


@middleware
def command_back_start(update, context):
    print('asddsadasdfasfafsFASDGA')
    dp = Dispatcher.get_instance()
    update.message.text = '/start'
    check = start.start_conversation.check_update(update)
    start.start_conversation.handle_update(update, dp, check, context)
    return ConversationHandler.END


command_delete_conversation = ConversationHandler(
    entry_points=[MessageHandler(to_filter_regex(texts.DELETE_COMMAND), command_delete)],
    states={
        states.DELETE_CONFIRM: [
            MessageHandler(to_filter_regex(texts.DELETE_COMMAND_CONFIRM), command_delete),
            MessageHandler(to_filter_regex(texts.SHOW_ANSWER), command_show_answer),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)],
)


command_menu_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.command, command_menu)],
    states={
        states.CHOOSE_COMMAND_OPTION: [
            MessageHandler(to_filter_regex(texts.DELETE_COMMAND), command_delete_conversation),
            MessageHandler(to_filter_regex(texts.SHOW_ANSWER), command_show_answer),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)],
)


command_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.all, commands_list)],
    states={
        states.COMMAND_MENU: [
            # command_menu_conversation,
            # command_addition.command_add_conversation,
            # MessageHandler(to_filter_regex(texts.back_text('start')), command_back_start)
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)],
)
