import telegram
from telegram.ext import Filters, CallbackQueryHandler, MessageHandler, ConversationHandler

from main import texts, keyboards
from main.models import User
from member.models import Bot


def connect_bot(bot, update):
    ''' Connect bot handler method called with inline keyboard '''
    query = update.callback_query

    query.answer()
    query.edit_message_text(texts.BOT_CONNECT, reply_markup=keyboards.CANCEL_START_M, parse_mode='MARKDOWN')

    return 1


def token(bot, update):
    '''
    Add bot with sent token
    If token is invalid edit text with error
    Otherwise save bot to database and return bot profile
    '''
    user = User.objects.get(id=update.effective_user.id)
    token = update.message.text

    bot.edit_message_text(
        chat_id=user.id,
        message_id=user.dialog_id,
        text=texts.SEARCHING_BOT,
    )

    telegram_bot = telegram.Bot(token)
    try:
        bot_user = telegram_bot.get_me()
    except Exception:
        text = texts.TOKEN_INVALID
        markup = keyboards.CANCEL_START_M
    else:
        connected_bot = Bot.objects.filter(username=bot_user.username).first()
        if connected_bot:
            connected_bot.token = token
            connected_bot.name = bot_user.name
            connected_bot.user = user
            connected_bot.save()
        else:
            connected_bot = Bot.objects.create(
                id=bot_user.id,
                owner=user,
                token=token,
                name=bot_user.name,
                username=bot_user.username,
            )
        text = texts.BOT_CONNECTED + texts.bot_profile(connected_bot.name)
        markup = keyboards.bot_profile_markup(connected_bot)

    try:
        sent_message = bot.send_message(
            chat_id=user.id,
            message_id=user.dialog_id,
            text=text,
            reply_markup=markup,
            parse_mode='MARKDOWN'
        )
        user.update_dialog(bot, sent_message.message_id)
    except Exception:
        pass

    update.message.delete()


connect_bot_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(connect_bot, pattern='connect_bot')],
    states={
        1: [MessageHandler(Filters.regex(r'\d*:.*'), token)],
    },
    fallbacks=[],
)
