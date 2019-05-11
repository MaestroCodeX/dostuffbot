from telegram.ext import CallbackQueryHandler, Dispatcher, ConversationHandler, MessageHandler, Filters
from django.conf import settings

from core.enums import CommandStatus
from core.handlers import ignore
from member import texts, keyboards, states
from member.middleware import middleware
from member.models import Command
from member.utils import (
    call_command_regex,
    get_command_from_call,
    get_command_id_from_call,
)


@middleware
def commands_list(update, context):
    ''' Callback function to show all commands. '''

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
    ''' Callback function to show command menu that was chosen from the list. '''
    caller = update.message.text
    command = Command.objects.get(caller=caller)
    update.message.reply_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(),
        parse_mode='MARKDOWN',
    )

    context.chat_data['cmd_id'] = command.id


@middleware
def command_delete(update, context):
    ''' Handle delete button in command menu.
    Do not delete the command but send confirmation request. '''
    command_id = context.chat_data['cmd_id']
    command = Command.objects.get(id=command_id)
    text = texts.delete_command(command)
    markup = keyboards.confirm_deletion_markup(command)

    update.message.reply_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')


@middleware
def command_edit_caller(update, context):
    ''' Callback function to handle edit command button. '''
    query = update.callback_query

    command_id = get_command_id_from_call(query.data)
    query.edit_message_text(
        text='Send me a new command.',
        reply_markup=keyboards.back_command_menu_markup(command_id),
        parse_mode='MARKDOWN',
    )


@middleware
def command_edit_caller_sent(update, context):
    ''' Callback function to handle editing commmand state when caller text was sent. '''
    caller = update.message.text
    db_bot = context.bot.db_bot

    if Command.objects.filter(bot=db_bot, caller=caller).exists():
        update.message.reply_text(f'The command {caller} already exists.')

    command = Command.objects.filter(bot=db_bot, status=CommandStatus.EDIT_CALLER).first()
    command.caller = caller
    command.save()
    update.message.reply_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(command),
        parse_mode='MARKDOWN',
    )


@middleware
def command_delete_confirm(update, context):
    ''' Handle delete confirmation button.
    Delete the command and return user to commands list. '''
    query = update.callback_query

    command = get_command_from_call(context.bot, query.data)
    dp = Dispatcher.get_instance()
    handlers = dp.handlers[settings.DEFAULT_HANDLER_GROUP]
    for handler in handlers:
        print(handler.filters)
    command.delete()

    query.answer('The command has disappeared...')
    commands_list(context.bot, update)


def command_show_answer(update, context):
    query = update.callback_query

    command = get_command_from_call(context.bot, query.data)
    command.reply_to(query.message)

    query.message.reply_text(
        'The full answer is shown. Select what you want to do next:',
        reply_markup=keyboards.command_shown_markup(command)
    )


command_menu_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.command, command_menu)],
    states={
        states.COMMANDS_DELETE: [
            MessageHandler(Filters.regex('^Delete command$'), command_delete),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)],
)


command_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^Commands$'), commands_list)],
    states={
        states.COMMAND_MENU: [
            command_menu_conv,
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)],
)

commands_list_handler = CallbackQueryHandler(commands_list, pattern='commands_list')
command_menu_handler = CallbackQueryHandler(command_menu, pattern=call_command_regex('menu'))
command_delete_handler = CallbackQueryHandler(command_delete, pattern=call_command_regex('delete'))
command_show_answer_handler = CallbackQueryHandler(command_show_answer, pattern=call_command_regex('show_answer'))
command_delete_confirm_handler = CallbackQueryHandler(
    command_delete_confirm,
    pattern=call_command_regex('delete_confirm'),
)
command_edit_caller_handler = CallbackQueryHandler(command_edit_caller, pattern=call_command_regex('edit_caller'))
