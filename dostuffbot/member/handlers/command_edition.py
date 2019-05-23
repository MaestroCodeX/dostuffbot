from core.enums import CommandMutationMode
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
    context.chat_data['cmd_instance_edit'] = context.chat_data['cmd_instance']
    context.chat_data['retutn_state'] = states.SEND_EDIT_MESSAGE
    context.chat_data['mode'] = CommandMutationMode.EDITING

    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def delete_all_messages(update, context):
    context.chat_data['msgs_to_delete'] = ALL
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def delete_last_message(update, context):
    command = context.chat_data['cmd_instance']
    msgs_to_delete = context.chat_data['msgs_to_delete']
    try:
        msg = command.command_messages.exclude(id__in=msgs_to_delete).latest('id')
        context.chat_data['msgs_to_delete'].append(msg.id)
    except CommandMessage.DoesNotExist:
        pass
    inform_number_of_commands(update, context)
    return states.SEND_EDIT_MESSAGE


@middleware
def save_changes(update, context):
    msgs_to_delete = context.chat_data['msgs_to_delete']
    if len(msgs_to_delete) > 0:
        update.message.reply_text(
            text='Are you sure you want to save changes?',
            reply_markup=keyboards.confirm_yes_no_markup(),
            parse_mode='MARKDOWN',
        )
    else:
        save_changes_confirmed(update, context)

    return states.EXIT_WITH_SAVE_CONFIRM


@middleware
def save_changes_confirmed(update, context):
    command = context.chat_data['cmd_instance']
    msgs_to_delete = context.chat_data.pop('msgs_to_delete')
    if msgs_to_delete == ALL:
        command.command_messages.all().update(is_active=False)
    else:
        CommandMessage.objects.filter(id__in=msgs_to_delete).update(is_active=False)
    update.message.reply_text('Selected messages were deleted.')
    return commands.command_menu(update, context)


@middleware
def exit_no_save(update, context):
    update.message.reply_text(
        text='Are you sure you want to exit without any changes?',
        reply_markup=keyboards.confirm_yes_no_markup(),
        parse_mode='MARKDOWN',
    )

    return states.EXIT_NO_SAVE_CONFIRM


@middleware
def exit_no_save_confirmed(update, context):
    del context.chat_data['msgs_to_delete']
    return commands.command_menu(update, context)


@middleware
def exit_declined(update, context):
    return command_edit_answer(update, context)


def inform_number_of_commands(update, context):
    command = context.chat_data['cmd_instance']
    msgs_to_delete = context.chat_data['msgs_to_delete']
    left_count = 0
    if msgs_to_delete != ALL:
        count = command.command_messages.count()
        left_count = count - len(msgs_to_delete)
    text = f'The command {command.caller} has {left_count} message{"s" if left_count > 1 else ""}.'
    update.message.reply_text(text=text)
