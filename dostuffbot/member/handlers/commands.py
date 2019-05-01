from telegram.ext import CallbackQueryHandler, Dispatcher, ConversationHandler, MessageHandler, Filters, CommandHandler

from core.enums import CommandMessageType
from member import texts, keyboards
from member.middleware import middleware
from member.models import Command, CommandMessage
from member.utils import (
    call_command_regex,
    command_handler,
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

    return 1


@middleware
def command_add_caller(bot, update):
    caller = update.message.text

    if Command.objects.filter(caller=caller).exists():
        update.message.reply_text(f'The command {caller} already exists.')
        return 1

    Command.objects.create(caller=caller)

    update.message.reply_text(
        f'Now send me everything that bot will answer when user types {caller}',
    )

    return 2


@middleware
def command_add_caller_invalid(bot, update):
    update.message.reply_text(
        'The command should start with / and can only contain [a-Z] letters, [0-9] numbers and [_] underscores',
    )
    return 1


@middleware
def command_add_message(bot, update):
    text = update.message.text
    command = Command.objects.latest('id')
    CommandMessage.objects.create(command=command, type=CommandMessageType.TEXT, text=text)
    update.message.reply_text(
        'Message saved. Continue sending messsages or /complete to save the command.',
    )

    return 2


@middleware
def command_add_complete(bot, update):
    update.message.reply_text(
        'Congratulations! The command was added to your bot.',
    )
    command = Command.objects.latest('id')
    handler = command_handler(command)
    dp = Dispatcher.get_instance()
    dp.add_handler(handler)
    commands = Command.objects.all()
    update.message.reply_text(
        'This is a list of your commands. Select command to see the details:',
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )
    return ConversationHandler.END


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


def idle(bot, update):
    pass


commands_list_handler = CallbackQueryHandler(commands_list, pattern='commands_list')
command_menu_handler = CallbackQueryHandler(command_menu, pattern=call_command_regex('menu'))
command_delete_handler = CallbackQueryHandler(command_delete, pattern=call_command_regex('delete'))
command_delete_confirm_handler = CallbackQueryHandler(
    command_delete_confirm,
    pattern=call_command_regex('delete_confirm'),
)
command_edit_handlers = CallbackQueryHandler(command_edit, pattern=call_command_regex('edit'))
command_add_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(command_add, pattern='command_add')],
    states={
        1: [
            MessageHandler(Filters.command, command_add_caller),
            MessageHandler(Filters.text, command_add_caller_invalid),
        ],
        2: [
            MessageHandler(Filters.text, command_add_message),
            CommandHandler('complete', command_add_complete),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, idle)]
)
