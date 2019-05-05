from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from main import texts, keyboards
from main.handlers import management
from main.models import User
from main.utils import get_or_create_user, log_exception, call_bot_regex


@log_exception
@run_async
def start_command(bot, update):
    ''' The start was called with /start '''
    message = update.message
    user = get_or_create_user(message)
    args = update.message.text.split()[1:]
    if args:
        handle_deeplink(bot, update, args)
        # break further execution as soon as user did't want to send start command
        return

    context = {
        'text': texts.START,
        'reply_markup': keyboards.START_M,
        'parse_mode': 'MARKDOWN',
    }
    user.update_dialog(bot, message.reply_text, context)

    update.effective_message.delete()


def start(bot, update):
    '''
    The start was called with inline keyboard.
    Delete old dialog message and send new one
    so that chat with the bot gets to the top of all chats list.
    '''
    query = update.callback_query

    user = User.objects.get(id=update.effective_user.id)

    context = {
        'text': texts.START,
        'reply_markup': keyboards.START_M,
        'parse_mode': 'MARKDOWN',
    }
    user.update_dialog(bot, query.message.reply_text, context)


def handle_deeplink(bot, update, args):
    command = args[0]
    if call_bot_regex('profile').match(command):
        management.bot_profile_command(bot, update)


start_command_handler = CommandHandler('start', start_command)
start_handler = CallbackQueryHandler(start, pattern='start')
