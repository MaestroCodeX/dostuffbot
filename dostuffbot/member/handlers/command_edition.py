from core.enums import CommandMessageType, EditLastAction
from member import texts, keyboards, states
from member.handlers import commands
from member.middleware import middleware
from member.models import Command, CommandMessage

ALL = '__all__'


@middleware
def command_edit_caller(update, context):
    """ Callback function to handle edit command button. """
    update.message.reply_text(
        text='Okay, send me a new command.',
        reply_markup=keyboards.back_markup('command menu'),
        parse_mode='MARKDOWN',
    )
    return states.INPUT_EDIT_CALLER


@middleware
def command_edit_caller_sent(update, context):
    """ Callback function to handle editing commmand state when caller text was sent. """
    caller = update.message.text
    db_bot = context.bot.db_bot

    if Command.objects.filter(bot=db_bot, caller=caller).exists():
        update.message.reply_text(f'The command {caller} already exists.')
        return states.INPUT_CALLER

    command = context.chat_data['cmd_instance']
    command.caller = caller
    command.save()

    update.message.reply_text('Command was successfully updated!')
    update.message.reply_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(),
        parse_mode='MARKDOWN',
    )

    return states.CHOOSE_COMMAND_OPTION


@middleware
def command_edit_answer(update, context):
    """ Callback function to handle edit command button. """
    text = (
        '___DESCRIPTION___: You are in command editting mode. '
        'You can either send new messages to add them '
        'or delete your previous messages.\n\n'
        '___ATTEINTION___: No changes will be affected unless you hit '
        f'___{"Save changes"}___ button.'
    )
    update.message.reply_text(
        text=text,
        reply_markup=keyboards.edit_asnwer_markup(),
        parse_mode='MARKDOWN',
    )
    context.chat_data['msgs_to_delete'] = []
    context.chat_data['last_edit_action'] = None

    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


def commit_last_action(context):
    last_action = context.chat_data.pop('last_edit_action', None)
    command = context.chat_data['cmd_instance']
    if last_action == EditLastAction.DELETE_ALL:
        command.command_messages.all().update(is_active=False)
    elif last_action == EditLastAction.DELETE_LAST:
        try:
            command.command_messages.latest('id').delete()
        except CommandMessage.DoesNotExist:
            pass


@middleware
def undo_last_action(update, context):
    last_action = context.chat_data.pop('last_edit_action', None)
    command = context.chat_data['cmd_instance']
    response = 'No last action found.'

    if last_action == EditLastAction.DELETE_ALL:
        response = 'All deleted messages were recovered.'
    elif last_action == EditLastAction.DELETE_LAST:
        response = 'Last deleted message was recovered.'
    elif last_action == EditLastAction.ADD_MESSAGE:
        response = 'Last added message was deleted.'
        try:
            command.command_messages.latest('id').delete()
        except CommandMessage.DoesNotExist:
            pass

    update.message.reply_text(response)
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def delete_all_messages(update, context):
    commit_last_action(context)
    context.chat_data['last_edit_action'] = EditLastAction.DELETE_ALL
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def delete_last_message(update, context):
    commit_last_action(context)
    context.chat_data['last_edit_action'] = EditLastAction.DELETE_LAST
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def exit_edit_mode(update, context):
    commit_last_action(context)
    del context.chat_data['msgs_to_delete']
    del context.chat_data['last_edit_action']
    return commands.command_menu()


def inform_number_of_commands(update, context):
    command = context.chat_data['cmd_instance']
    last_action = context.chat_data.get('last_edit_action')
    count = command.command_messages.count()
    if last_action == EditLastAction.DELETE_LAST:
        count -= 1
    elif last_action == EditLastAction.DELETE_ALL:
        count = 0

    text = f'The command {command.caller} has {count} message{"s" if count > 1 else ""}.'
    update.message.reply_text(text=text)


@middleware
def command_add_text(update, context):
    """ Callback function to handle message for command. Returns its state to make the process repetitive. """
    text = update.message.text
    command = context.chat_data['cmd_instance']
    CommandMessage.objects.create(
        command=command,
        type=CommandMessageType.TEXT,
        text=text,
    )
    return continue_command_adding(update, context)


def command_add_media_message(context, update, file_id, media_type):
    command = context.chat_data['cmd_instance']
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
        'The location messages are still being developed. It will be support at an early future.',
    )
    return continue_command_adding(update, context)


def continue_command_adding(update, context, silence=False):
    context.chat_data['last_edit_action'] = EditLastAction.ADD_MESSAGE
    if not silence:
        update.message.reply_text(
            'Message saved. Continue sending messsages or hit "Complete" to save the command.',
        )

    return states.SEND_EDIT_MESSAGE
