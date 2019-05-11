from telegram.ext import CallbackQueryHandler, Dispatcher, ConversationHandler, MessageHandler, Filters

from core.enums import CommandMessageType, CommandStatus
from core.handlers import ignore
from member import texts, keyboards, states
from member.middleware import middleware
from member.models import Command, CommandMessage
from member.utils import get_command_handler


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

    return states.SEND_CALLER


@middleware
def command_add_caller(bot, update):
    ''' Callback function to handle message with command caller. '''
    caller = update.message.text

    if len(caller) > 32:
        update.message.reply_text(f'Ensure your command length is less than 32 characters.')
        return states.SEND_CALLER

    if Command.objects.filter(bot=bot.db_bot, caller=caller).exists():
        update.message.reply_text(f'The command {caller} already exists.')
        return states.SEND_CALLER

    Command.objects.filter(bot=bot.db_bot, status=CommandStatus.DONE).delete()
    Command.objects.create(bot=bot.db_bot, caller=caller, status=CommandStatus.EDIT_ANSWER)

    update.message.reply_text(
        f'Now send me everything that bot will answer when user types {caller}',
    )

    return states.SEND_MESSAGE


@middleware
def command_add_caller_invalid(bot, update):
    ''' Callback function to handle message when command is invalid. '''
    text = (
        'The command should start with /\n'
        'Max. length is 32 characters.\n'
        'The command can only contain:'
        '\n - letters\n - numbers\n - "_"'
    )
    update.message.reply_text(text)

    return states.SEND_CALLER


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

    return states.SEND_MESSAGE


@middleware
def command_add_complete(bot, update):
    ''' Callback function to handle /complete command to finish command adding. '''
    command = get_command_to_edit(bot.db_bot)
    command.status = CommandStatus.DONE
    command.save()

    handler = get_command_handler(command)
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


def command_add_cancel(update, context):
    command = get_command_to_edit(context.bot.db_bot)
    command.delete()
    update.message.reply_text(
        'The command addition was cancelled.',
    )
    return ConversationHandler.END


command_add_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(command_add, pattern='command_add')],
    states={
        states.SEND_CALLER: [
            MessageHandler(Filters.command, command_add_caller),
            MessageHandler(Filters.text, command_add_caller_invalid),
        ],
        states.SEND_MESSAGE: [
            MessageHandler(Filters.text, command_add_text),
            MessageHandler(Filters.photo, command_add_photo),
            MessageHandler(Filters.video, command_add_video),
            MessageHandler(Filters.document, command_add_document),
            MessageHandler(Filters.audio, command_add_audio),
            MessageHandler(Filters.voice, command_add_voice),
            MessageHandler(Filters.location, command_add_location),
            MessageHandler('Complete', command_add_complete),
            MessageHandler('Cancel', command_add_cancel),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)]
)
