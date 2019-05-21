from member import texts, keyboards, states
from member.middleware import middleware
from member.models import Command


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
    command = context.chat_data['cmd_instance']
    inform_number_of_commands(update, command)
    return states.SEND_EDIT_MESSAGE


@middleware
def delete_all_messages(update, context):
    pass


@middleware
def delete_last_message(update, context):
    pass


@middleware
def save_changes(update, context):
    pass


@middleware
def exit_no_save(update, context):
    pass


def inform_number_of_commands(update, command):
    count = command.command_messages.count()
    text = f'The command {command.caller} has {count} command{"s" if count > 1 else ""}.'
    update.message.reply_text(text=text)
