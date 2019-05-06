from telegram.ext import Filters, MessageHandler, ConversationHandler, CallbackQueryHandler

from member import texts, keyboards
from member.handlers import start
from member.middleware import middleware
from member.models import Subscriber

SEND_MESSAGE = range(1)


@middleware
def notify_claim(bot, update):
    ''' Callback function when user wants to send message to his subscribers. '''

    query = update.callback_query
    query.edit_message_text(
        'Send me a message that you want to share with your subscribers.',
        reply_markup=keyboards.back_markup('menu', 'start'),
    )

    return SEND_MESSAGE


def notify_subscribers_with_text(bot, subs, message):
    ''' Function to send notification to user from given queryset.
    Also keeps editing a message for admin with counter. '''

    text_status = texts.message_mailing_status(0, subs.count())
    status_message = message.reply_text(text_status)
    for i, sub in enumerate(subs, 1):
        bot.send_message(chat_id=sub.id, text=message.text)
        text_status = texts.message_mailing_status(i, subs.count())
        status_message.edit_text(text_status)
    status_message.edit_text(texts.notification_sent(subs.count(), subs.count()))


@middleware
def notify_subcribers(bot, update):
    ''' Callback function when user sent message with a text for a notification.
    Send a message to all subscribers and return user to start menu. '''

    subs = Subscriber.objects.filter(bot=bot.db_bot)
    message = update.message
    notify_subscribers_with_text(bot, subs, message)
    start.start(bot, update)

    return ConversationHandler.END


notify_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(notify_claim, pattern='^notify$')],
    states={
        SEND_MESSAGE: [
            MessageHandler(Filters.text, notify_subcribers),
        ],
    },
    fallbacks=[],
    allow_reentry=True,
)
