from core.enums import DeepCommand
from core.utils import get_reply_function
from member import keyboards, states
from member.handlers import commands
from member.middleware import middleware
from member.utils import admin_only


@admin_only
@middleware
def start(update, context):
    """ Callback function when user sends /start or returns to main menu.
    It also handles start command with arguments from main bot. """

    if update.message:
        parts = update.message.text.split()
        args = parts[1:]
        if parts[0] == '/start' and args:
            handle_deeplink(context.bot, update, args)
            # break further execution as soon as user did't want to send start command
            return

    reply_func = get_reply_function(update)
    if not reply_func:
        return

    reply_func(
        'Choose an option from the list below:',
        reply_markup=keyboards.start_markup(),
        parse_mode='MARKDOWN',
    )

    return states.START_MENU


def handle_deeplink(bot, update, args):
    command = args[0]

    if command == DeepCommand.COMMANDS:
        commands.commands_list(bot, update)
