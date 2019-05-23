from core.enums import DeepCommand
from member import keyboards, states
from member.handlers import commands
from member.middleware import middleware
from member.utils import admin_only


@admin_only
@middleware
def start(update, context):
    """ Callback function when user sends /start or returns to main menu.
    It also handles start command with arguments from main bot. """

    context.chat_data = {}

    if update.message:
        parts = update.message.text.split()
        args = parts[1:]
        if parts[0] == '/start' and args:
            handle_deeplink(update, context, args)
            # break further execution as soon as user did't want to send start command
            return

    update.message.reply_text(
        'Choose an option from the list below:',
        reply_markup=keyboards.start_markup(),
        parse_mode='MARKDOWN',
    )

    return states.START_MENU


def handle_deeplink(update, context, args):
    if args[0] == DeepCommand.COMMANDS:
        commands.commands_list(update, context)
