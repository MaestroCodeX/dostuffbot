from telegram.ext import CallbackQueryHandler, Dispatcher, ConversationHandler, MessageHandler, Filters, CommandHandler
from django.conf import settings

from core.enums import CommandMessageType, CommandStatus
from core.utils import get_reply_function
from member import texts, keyboards
from member.middleware import middleware
from member.models import Command, CommandMessage
from member.utils import (
    call_command_regex,
    command_handler,
    get_command_from_call,
    get_command_id_from_call,
)

SEND_CALLER, SEND_MESSAGE = range(2)


@middleware
def commands_list(bot, update):
    ''' Callback function to show all commands. '''
    reply_func = get_reply_function(update)
    if not reply_func:
        return

    commands = Command.objects.filter(bot=bot.db_bot, status=CommandStatus.DONE)
    text = 'This is a list of your commands. Select command to see the details:'
    if not commands:
        text = 'Press "Add command" to create your first command.'

    reply_func(
        text,
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )


@middleware
def command_menu(bot, update):
    ''' Callback function to show command menu that was chosen from the list. '''
    query = update.callback_query
    command = get_command_from_call(bot, query.data)
    query.edit_message_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(command),
        parse_mode='MARKDOWN',
    )


@middleware
def command_add(bot, update):
    ''' Callback function to handle 'Add command' button. '''
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

    return SEND_CALLER


@middleware
def command_add_caller(bot, update):
    ''' Callback function to handle message with command caller. '''
    caller = update.message.text

    if len(caller) > 32:
        update.message.reply_text(f'Ensure your command length is less than 32 characters.')
        return SEND_CALLER

    if Command.objects.filter(bot=bot.db_bot, caller=caller).exists():
        update.message.reply_text(f'The command {caller} already exists.')
        return SEND_CALLER

    Command.objects.filter(bot=bot.db_bot, status=CommandStatus.DONE).delete()
    Command.objects.create(bot=bot.db_bot, caller=caller, status=CommandStatus.EDIT_ANSWER)

    update.message.reply_text(
        f'Now send me everything that bot will answer when user types {caller}',
    )

    return SEND_MESSAGE


@middleware
def command_add_caller_invalid(bot, update):
    ''' Callback function to handle message when command is invalid. '''
    text = (
        'The command should start with /\n'
        'Max. length is 32 characters.\n'
        'The command can only contain:'
        '\n - [a-Z] letters\n - [0-9] numbers\n - [_] underscores'
    )
    update.message.reply_text(text)

    return SEND_CALLER


def get_command_to_edit(bot):
    return Command.objects.filter(bot=bot, status=CommandStatus.EDIT_ANSWER).last()


@middleware
def command_add_text(bot, update):
    ''' Callback function to handle message for command. Returns its state to make the process repetitive. '''
    text = update.message.text
    command = get_command_to_edit(bot.db_bot)
    CommandMessage.objects.create(
        command=command,
        type=CommandMessageType.TEXT,
        text=text,
    )
    return continue_command_adding(update)


def command_add_media_message(bot, update, file_id, media_type):
    command = get_command_to_edit(bot.db_bot)
    CommandMessage.objects.create(
        command=command,
        type=media_type,
        text=update.message.caption,
        file_id=file_id,
    )


@middleware
def command_add_photo(bot, update):
    photo = update.message.photo[-1]
    command_add_media_message(bot, update, photo.file_id, CommandMessageType.PHOTO)
    return continue_command_adding(update)


@middleware
def command_add_video(bot, update):
    video = update.message.video
    command_add_media_message(bot, update, video.file_id, CommandMessageType.VIDEO)
    return continue_command_adding(update)


@middleware
def command_add_document(bot, update):
    document = update.message.document
    command_add_media_message(bot, update, document.file_id, CommandMessageType.DOCUMENT)
    return continue_command_adding(update)


@middleware
def command_add_audio(bot, update):
    audio = update.message.audio
    command_add_media_message(bot, update, audio.file_id, CommandMessageType.AUDIO)
    return continue_command_adding(update)


@middleware
def command_add_voice(bot, update):
    voice = update.message.voice
    command_add_media_message(bot, update, voice.file_id, CommandMessageType.VOICE)
    return continue_command_adding(update)


@middleware
def command_add_location(bot, update):
    update.message.reply_text(
        'The location messages are still being developed. It will be support at an early future.',
    )


def continue_command_adding(update, silence=False):
    if not silence:
        update.message.reply_text(
            'Message saved. Continue sending messsages or /complete to save the command.',
        )

    return SEND_MESSAGE


@middleware
def command_add_complete(bot, update):
    ''' Callback function to handle /complete command to finish command adding. '''
    command = get_command_to_edit(bot.db_bot)
    command.status = CommandStatus.DONE
    command.save()

    handler = command_handler(command)
    dp = Dispatcher.get_instance()
    dp.add_handler(handler)

    update.message.reply_text(
        'Congratulations! The command was added to your bot.',
    )

    commands = Command.objects.filter(bot=bot.db_bot, status=CommandStatus.DONE)
    update.message.reply_text(
        'This is a list of your commands. Select command to see the details:',
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )
    return ConversationHandler.END


@middleware
def command_delete(bot, update):
    ''' Handle delete button in command menu.
    Do not delete the command but send confirmation request. '''
    query = update.callback_query

    command = get_command_from_call(bot, query.data)
    text = texts.delete_command(command)
    markup = keyboards.confirm_deletion_markup(command)

    query.edit_message_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')


@middleware
def command_edit_caller(bot, update):
    ''' Callback function to handle edit command button. '''
    query = update.callback_query

    command_id = get_command_id_from_call(query.data)
    query.edit_message_text(
        text='Send me a new command.',
        reply_markup=keyboards.back_command_menu_markup(command_id),
        parse_mode='MARKDOWN',
    )


@middleware
def command_edit_caller_sent(bot, update):
    ''' Callback function to handle editing commmand state when caller text was sent. '''
    caller = update.message.text

    if Command.objects.filter(bot=bot.db_bot, caller=caller).exists():
        update.message.reply_text(f'The command {caller} already exists.')

    command = Command.objects.filter(bot=bot.db_bot, status=CommandStatus.EDIT_CALLER).first()
    command.caller = caller
    command.save()
    update.message.reply_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(command),
        parse_mode='MARKDOWN',
    )


@middleware
def command_delete_confirm(bot, update):
    ''' Handle delete confirmation button.
    Delete the command and return user to commands list. '''
    query = update.callback_query

    command = get_command_from_call(bot, query.data)
    dp = Dispatcher.get_instance()
    handlers = dp.handlers[settings.DEFAULT_HANDLER_GROUP]
    for handler in handlers:
        print(handler.filters)
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
command_edit_caller_handler = CallbackQueryHandler(command_edit_caller, pattern=call_command_regex('edit_caller'))
command_add_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(command_add, pattern='command_add')],
    states={
        SEND_CALLER: [
            MessageHandler(Filters.command, command_add_caller),
            MessageHandler(Filters.text, command_add_caller_invalid),
        ],
        SEND_MESSAGE: [
            MessageHandler(Filters.text, command_add_text),
            MessageHandler(Filters.photo, command_add_photo),
            MessageHandler(Filters.video, command_add_video),
            MessageHandler(Filters.document, command_add_document),
            MessageHandler(Filters.audio, command_add_audio),
            MessageHandler(Filters.voice, command_add_voice),
            MessageHandler(Filters.location, command_add_location),
            CommandHandler('complete', command_add_complete),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, idle)]
)
