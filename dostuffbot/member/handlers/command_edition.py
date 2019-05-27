from core.enums import CommandMessageType, EditLastAction
from member import texts, keyboards, states
from member.handlers import commands
from member.middleware import middleware
from member.models import Command, CommandMessage


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

    chat_data = context.chat_data

    text = (
        '___DESCRIPTION___: You are in command editting mode. '
        'You can either send new messages to add them '
        'or delete your previous messages.\n\n'
        '___ATTEINTION___: No changes will be affected unless you hit '
        '___Save changes___ button.'
    )
    update.message.reply_text(
        text=text,
        reply_markup=keyboards.edit_asnwer_markup(),
        parse_mode='MARKDOWN',
    )
    command = chat_data['cmd_instance']
    chat_data['edit_actions_log'] = []
    chat_data['msgs_count'] = command.message_set.count()

    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


def commit_all_actions(context):
    """ Commit all action that were added to logs and remove them. """

    chat_data = context.chat_data

    actions_to_commit = chat_data['edit_actions_log']
    chat_data['edit_actions_log'] = []
    command = chat_data['cmd_instance']
    for action in actions_to_commit:
        if action == EditLastAction.DELETE_ALL:
            command.message_set.all().update(is_active=False)

        elif action == EditLastAction.DELETE_LAST:
            try:
                command.message_set.latest('id').delete()
            except CommandMessage.DoesNotExist:
                pass


@middleware
def undo_last_action(update, context):
    """ Undo last action that was added to the logs. """

    chat_data = context.chat_data

    action_logs = chat_data['edit_actions_log']
    command = chat_data['cmd_instance']
    try:
        action = action_logs.pop()
    except IndexError:
        update.message.reply_text('No last action found.')
        return states.SEND_EDIT_MESSAGE

    response = ''
    if action == EditLastAction.DELETE_ALL:
        response = 'All deleted messages were recovered.'
        last_deletes_count = 0
        for a in action_logs:
            if a == EditLastAction.DELETE_LAST:
                last_deletes_count += 1
        chat_data['msgs_count'] = command.message_set.count() - last_deletes_count

    elif action == EditLastAction.DELETE_LAST:
        response = 'Last deleted message was recovered.'
        chat_data['msgs_count'] += 1

    elif action == EditLastAction.ADD_MESSAGE:
        response = 'Last added message was deleted.'
        try:
            command.message_set.latest('id').update(is_active=False)
            chat_data['msgs_count'] -= 1
        except CommandMessage.DoesNotExist:
            pass

    update.message.reply_text(response)
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def delete_all_messages(update, context):
    """ Set messages counter to 0 and inform user how much messages left. """

    chat_data = context.chat_data

    if chat_data['msgs_count'] == 0:
        update.message.reply_text('The command has no messages.')
        return states.SEND_EDIT_MESSAGE

    chat_data['edit_actions_log'].append(EditLastAction.DELETE_ALL)
    chat_data['msgs_count'] = 0
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def delete_last_message(update, context):
    """ Decrease messages counter by 1 and inform user how much messages left. """

    chat_data = context.chat_data

    if chat_data['msgs_count'] == 0:
        update.message.reply_text('The command has no messages.')
        return states.SEND_EDIT_MESSAGE

    chat_data['edit_actions_log'].append(EditLastAction.DELETE_LAST)
    chat_data['msgs_count'] -= 1
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def exit_edit_mode(update, context):
    """ Return user to command menu and commit all actions in logs. """

    commit_all_actions(context)
    del context.chat_data['edit_actions_log']
    return commands.command_menu(update, context)


def get_inform_message(update, context):
    """ Returns the text to inform the number of messages left. """
    chat_data = context.chat_data

    command = chat_data['cmd_instance']
    count = chat_data['msgs_count']
    text = f'The command {command.caller} has {count} message{"s" if count > 1 else ""}.'
    return text


def inform_number_of_commands(update, context):
    """ Sends down to user the number of messages left. """

    text = get_inform_message(update, context)
    update.message.reply_text(text=text)


@middleware
def command_add_text(update, context):
    """ Callback function to handle message for command. Returns its state to make the process repetitive. """

    chat_data = context.chat_data

    text = update.message.text
    command = chat_data['cmd_instance']
    CommandMessage.objects.create(
        command=command,
        type=CommandMessageType.TEXT,
        text=text,
    )
    chat_data['msgs_count'] += 1
    return continue_command_adding(update, context)


def command_add_media_message(context, update, file_id, media_type):
    """ Helper function to save media message to the database. """

    chat_data = context.chat_data

    command = chat_data['cmd_instance']
    CommandMessage.objects.create(
        command=command,
        type=media_type,
        text=update.message.caption,
        file_id=file_id,
    )
    chat_data['msgs_count'] += 1


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
    return continue_command_adding(update, context)


def continue_command_adding(update, context, silence=False):
    """ Inform client that the sent command was saved. """

    context.chat_data['edit_actions_log'].append(EditLastAction.ADD_MESSAGE)
    if not silence:
        text = 'Message saved. ' + get_inform_message(update, context)
        update.message.reply_text(text)

    return states.SEND_EDIT_MESSAGE
