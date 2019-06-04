from django.conf import settings

from core.enums import DeepCommand
from member import keyboards, states, texts
from member.handlers import commands
from member.middleware import middleware
from member.permissions import admin_only


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
            return handle_deeplink(update, context, args)

    update.message.reply_text(
        'Choose an option from the list below:',
        reply_markup=keyboards.start_markup(),
        parse_mode='MARKDOWN',
    )

    return states.START_MENU


def handle_deeplink(update, context, args):
    if args[0] == DeepCommand.COMMANDS:
        return commands.commands_list(update, context)


@admin_only
@middleware
def help(update, context):
    """ Callback function to /help command. Reset chat data and return user to start menu. """

    context.chat_data = {}

    text = (
        '***You are the admin of the bot.***\n\n'
        'You have a full control under the commands bot can answer to users '
        'that have started the conversation with it. You can add, edit and delete them. '
        f'To manage press "{texts.COMMANDS}"\n\n'
        f'You can also send a message to all active bot users by pressing "{texts.SEND_NOTIFICATION}"\n\n'
        f'___Powered by___ @{settings.MAIN_BOT_NAME}'
    )
    update.message.reply_text(
        text,
        reply_markup=keyboards.start_markup(),
        parse_mode='MARKDOWN',
    )

    return states.START_MENU
