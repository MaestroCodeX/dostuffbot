from member import texts, keyboards, states
from member.middleware import middleware
from member.models import Command


@middleware
def command_edit_caller(update, context):
    """ Callback function to handle edit command button. """
    update.message.reply_text(
        text='Send me a new command.',
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
