import telegram
from telegram import ParseMode
from telegram.ext import Filters, CallbackQueryHandler, MessageHandler

from main.models import User, Bot
from main.keyboards import cancel_start_markup, get_profile_markup
from main.texts import connect_bot_text, token_invalid_text, succesfully_connected_text


def connect_bot(bot, update):
    ''' Connect bot handler method called with inline keyboard '''
    query = update.callback_query

    query.answer()
    query.edit_message_text(connect_bot_text, reply_markup=cancel_start_markup, parse_mode=ParseMode.MARKDOWN)

    return 1


def token(bot, update):
    '''
    Add bot with sent token
    If token is invalid edit text with error
    Otherwise save bot to database and return bot profile
    '''
    user = User.objects.get(id=update.message.from_user.id)
    token = update.message.text

    telegram_bot = telegram.Bot(token)
    try:
        bot_user = telegram_bot.get_me()
    except Exception:
        text = token_invalid_text
        markup = cancel_start_markup
    else:
        connected_bot = Bot.objects.create(owner=user, token=token, name=bot_user.username)
        text = succesfully_connected_text
        markup = get_profile_markup(connected_bot)

    bot.edit_message_text(
        chat_id=user.id,
        message_id=user.dialog_id,
        text=text,
        reply_markup=markup,
    )

    update.message.delete()


connect_bot_handler = CallbackQueryHandler(connect_bot, pattern='connect_bot')
token_handler = MessageHandler(Filters.regex(r'\d*:.*'), token)
