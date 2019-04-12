from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from main import texts, keyboards
from main.models import User
from main.utils import get_or_create_user, log_exception


@log_exception
@run_async
def start_command(bot, update):
    ''' The start was called with /start '''
    message = update.message
    user = get_or_create_user(message)

    sent_message = message.reply_text(texts.START, reply_markup=keyboards.START_M, parse_mode='MARKDOWN')

    user.update_dialog(bot, sent_message.message_id)
    update.effective_message.delete()


def start(bot, update):
    '''
    The start was called with inline keyboard.
    Delete old dialog message and send new one
    so that chat with the bot gets to the top of all chats list.
    '''
    query = update.callback_query

    sent_message = query.message.reply_text(texts.START, reply_markup=keyboards.START_M, parse_mode='MARKDOWN')
    user = User.objects.get(id=update.effective_user.id)
    user.update_dialog(bot, sent_message.message_id)
    query.message.delete()


start_command_handler = CommandHandler('start', start_command)
start_handler = CallbackQueryHandler(start, pattern='start')
