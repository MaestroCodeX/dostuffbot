from telegram.ext import Filters, MessageHandler, ConversationHandler

from member import texts, keyboards
from member.handlers import start
from member.models import Subscriber
from member.utils import admin_only, middleware


@admin_only
@middleware
def notify_claim(bot, update):
    update.message.reply_text(
        texts.NOTIFY_MESSAGE,
        reply_markup=keyboards.CANCEL_M,
    )

    return 1


def _notify_subscribers(bot, subs, message):
    text_status = texts.message_mailing_status(0, subs.count())
    status_message = message.reply_text(text_status)
    for i, sub in enumerate(subs, 1):
        bot.send_message(chat_id=sub.id, text=message.text)
        text_status = texts.message_mailing_status(i, subs.count())
        status_message.edit_text(text_status)


@admin_only
@middleware
def notify_subcribers(bot, update):
    subs = Subscriber.objects.all()
    message = update.message
    _notify_subscribers(bot, subs, message)

    update.message.reply_text(texts.notification_sent(subs))

    return ConversationHandler.END


@admin_only
@middleware
def cancel_notification(bot, update):
    update.message.reply_text(texts.NOTIFICATION_CANCELLED)
    start.start(bot, update)
    return ConversationHandler.END


notify_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Send notification'), notify_claim)],
    states={
        1: [
            MessageHandler(Filters.regex('Cancel'), cancel_notification),
            MessageHandler(Filters.text, notify_subcribers),
        ],
    },
    fallbacks=[],
)
