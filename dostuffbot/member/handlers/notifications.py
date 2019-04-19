from django.utils.translation import ugettext as _
from telegram.ext import Filters, MessageHandler, ConversationHandler

from member.models import Subscriber
from member.utils import middleware


@middleware
def notify_claim(bot, update):
    update.message.reply_text(_('send_message_to_notify'))

    return 1


@middleware
def notify_subcribers(bot, update):
    subs = Subscriber.objects.all()
    message = update.message.text
    for sub in subs:
        bot.send_message(chat_id=sub.id, text=message)

    update.message.reply_text(f'Notification was sent to all {subs.count()} active subscribers.')

    return ConversationHandler.END


notify_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Send notification'), notify_claim)],
    states={
        1: [MessageHandler(Filters.text, notify_subcribers)],
    },
    fallbacks=[],
)
