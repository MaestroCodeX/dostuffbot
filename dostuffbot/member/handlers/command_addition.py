from telegram.ext import Dispatcher
from django.conf import settings

from core.enums import CommandMessageType, CommandStatus
from member import keyboards, states
from member.handlers import commands
from member.middleware import middleware
from member.models import Command, CommandMessage
from member.utils import get_command_handler


@middleware
def command_add(update, context):
    """ Callback function to handle 'Add command' button. """

    commands_count = Command.objects.filter(bot=context.bot.db_bot).count()
    if commands_count >= settings.MAX_MEMBER_COMMANDS:
        update.message.reply_text((
            'You have reached the maximum number of available commands. '
            'If you want to add a new command, delete the old one or contact '
            'the [support](https://t.me/Dostuffsupportbot) '
            'to increase the limit of allowed commands.'
        ), parse_mode='MARKDOWN')
        return states.COMMAND_MENU

    text = (
        'Now send a command that you want to add.\n\n'
        'Here are some examples:\n'
        '/start\n/help\n/about\\_project\n/chapter\\_3'
    )
    update.message.reply_text(
        text,
        reply_markup=keyboards.cancel_markup(),
        parse_mode='MARKDOWN',
    )

    return states.INPUT_CALLER


@middleware
def command_add_caller(update, context):
    """ Callback function to handle message with command caller. """

    caller = update.message.text
    db_bot = context.bot.db_bot

    if len(caller) > 32:
        update.message.reply_text(f'Ensure your command length is less than 32 characters.')
        return states.INPUT_CALLER

    if Command.objects.filter(bot=db_bot, caller=caller).exists():
        update.message.reply_text(f'The command {caller} already exists.')
        return states.INPUT_CALLER

    Command.all.filter(bot=db_bot, status=CommandStatus.EDIT_ANSWER).delete()
    command = Command.objects.create(bot=db_bot, caller=caller, status=CommandStatus.EDIT_ANSWER)
    context.chat_data['cmd_instance_edit'] = command

    update.message.reply_text(
        f'Now send me everything that bot will answer when user types {caller}',
        reply_markup=keyboards.command_adding_markup()
    )

    return states.SEND_MESSAGE


@middleware
def command_add_caller_invalid(update, context):
    """ Callback function to handle message when command is invalid. """

    text = (
        'The ___command___ should start with /\n\n'
        '***The command can only contain:***'
        '\n - letters\n - numbers\n - \\_'
    )
    update.message.reply_text(text, parse_mode='MARKDOWN')

    return states.INPUT_CALLER


@middleware
def command_add_complete(update, context):
    """ Callback function to handle /complete command to finish command adding. """

    command = context.chat_data['cmd_instance_edit']
    if command.message_set.count() == 0:
        update.message.reply_text(
            'Please, add at least one message before saving the command.',
        )
        return states.SEND_MESSAGE
    command.status = CommandStatus.DONE
    command.save()
    del context.chat_data['cmd_instance_edit']

    handler = get_command_handler(command)
    dp = Dispatcher.get_instance()
    dp.add_handler(handler)

    update.message.reply_text(
        'Congratulations! The command was added to your bot.',
    )

    return commands.commands_list(update, context)


def command_add_cancel(update, context):
    command = context.chat_data.pop('cmd_instance_edit')
    command.delete()
    update.message.reply_text(
        'The command addition was cancelled.',
    )

    return commands.commands_list(update, context)


@middleware
def command_add_text(update, context):
    """ Callback function to handle message for command. Returns its state to make the process repetitive. """

    text = update.message.text
    command = context.chat_data['cmd_instance_edit']
    CommandMessage.objects.create(
        command=command,
        type=CommandMessageType.TEXT,
        text=text,
    )
    return continue_command_adding(update, context)


def command_add_media_message(context, update, file_id, media_type):
    command = context.chat_data['cmd_instance_edit']
    CommandMessage.objects.create(
        command=command,
        type=media_type,
        text=update.message.caption,
        file_id=file_id,
    )


@middleware
def command_add_photo(update, context):
    photo = update.message.photo[-1]
    command_add_media_message(context, update, photo.file_id, CommandMessageType.PHOTO)
    return continue_command_adding(update, context)


@middleware
def command_add_video(update, context):
    video = update.message.video
    command_add_media_message(context, update, video.file_id, CommandMessageType.VIDEO)
    return continue_command_adding(update, context)


@middleware
def command_add_document(update, context):
    document = update.message.document
    command_add_media_message(context, update, document.file_id, CommandMessageType.DOCUMENT)
    return continue_command_adding(update, context)


@middleware
def command_add_audio(update, context):
    audio = update.message.audio
    command_add_media_message(context, update, audio.file_id, CommandMessageType.AUDIO)
    return continue_command_adding(update, context)


@middleware
def command_add_voice(update, context):
    voice = update.message.voice
    command_add_media_message(context, update, voice.file_id, CommandMessageType.VOICE)
    return continue_command_adding(update, context)


@middleware
def command_add_location(update, context):
    update.message.reply_text(
        'The location messages are still being developed. It will be supported at an early future.',
    )


def continue_command_adding(update, context, silence=False):
    if not silence:
        update.message.reply_text(
            'Message saved. Continue sending messsages or hit "Complete" to save the command.',
        )

    return states.SEND_MESSAGE
