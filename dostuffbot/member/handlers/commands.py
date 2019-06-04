from member import texts, keyboards, states
from member.middleware import middleware
from member.models import Command


@middleware
def commands_list(update, context):
    """ Show a list of all commands. """

    chat_data = context.chat_data
    if 'cmd_instance' in chat_data:
        del chat_data['cmd_instance']

    commands = Command.objects.filter(bot=context.bot.db_bot)
    text = 'This is a list of your commands. Select command to see the details:'
    if not commands:
        text = 'Hit "Add command" to create your first command.'

    update.message.reply_text(
        text,
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )

    return states.COMMAND_MENU


@middleware
def command_menu(update, context):
    """ Show command menu that was chosen from the list. """

    command = context.chat_data.get('cmd_instance')
    if not command:
        caller = update.message.text
        try:
            command = Command.objects.get(caller=caller)
        except Command.DoesNotExist:
            return states.COMMAND_MENU
        context.chat_data['cmd_instance'] = command

    update.message.reply_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(),
        parse_mode='MARKDOWN',
    )
    return states.CHOOSE_COMMAND_OPTION


@middleware
def command_show_answer(update, context):
    command = context.chat_data['cmd_instance']
    command.reply_to(update.message)
    return states.CHOOSE_COMMAND_OPTION
