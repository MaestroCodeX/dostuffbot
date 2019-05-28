from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from core.utils import get_user_from_request
from main import texts, keyboards
from main.handlers import management
from main.utils import get_or_create_user, log_exception, call_bot_regex


@log_exception
@run_async
def start_command(update, context):
    """ The start was called with /start """
    message = update.message
    user = get_user_from_request(update, context)
    args = update.message.text.split()[1:]
    if args:
        success = handle_deeplink(update, context, args)
        # break further execution if handler returned True as soon as user did't want to send start command
        if success:
            return

    msg_context = {
        'text': texts.START,
        'reply_markup': keyboards.START_M,
        'parse_mode': 'MARKDOWN',
    }
    user.update_dialog(context.bot, message.reply_text, msg_context)

    update.effective_message.delete()


def start(update, context):
    """
    The start was called with inline keyboard.
    Delete old dialog message and send new one
    so that chat with the bot gets to the top of all chats list.
    """
    query = update.callback_query

    user = get_user_from_request(update, context)

    msg_context = {
        'text': texts.START,
        'reply_markup': keyboards.START_M,
        'parse_mode': 'MARKDOWN',
    }
    if user.is_dialog_on_top:
        query.edit_message_text(**msg_context)
    else:
        user.update_dialog(context.bot, query.message.reply_text, msg_context)


def handle_deeplink(update, context, args):
    command = args[0]
    if call_bot_regex('profile').match(command):
        try:
            management.bot_profile_command(update, context)
            return True
        except Exception:
            pass
    return False


start_command_handler = CommandHandler('start', start_command)
start_handler = CallbackQueryHandler(start, pattern='start')
