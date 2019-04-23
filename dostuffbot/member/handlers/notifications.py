from telegram.ext import Filters, MessageHandler, ConversationHandler

from member import texts
from member.models import Subscriber
from member.utils import admin_only, middleware


@admin_only
@middleware
def notify_claim(bot, update):
    update.message.reply_text(texts.NOTIFY_MESSAGE)

    return 1


@admin_only
@middleware
def notify_subcribers(bot, update):
    subs = Subscriber.objects.all()
    message = update.message.text
    for sub in subs:
        bot.send_message(chat_id=sub.id, text=message)

    update.message.reply_text(texts.notification_sent(subs))

    return ConversationHandler.END


notify_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Send notification'), notify_claim)],
    states={
        1: [MessageHandler(Filters.text, notify_subcribers)],
    },
    fallbacks=[],
)
