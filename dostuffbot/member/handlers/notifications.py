from telegram.ext import Filters, MessageHandler, ConversationHandler

from member.models import Subscriber


def notify_claim(bot, update):
    update.message.reply_text(f'Send a message that you want to share with your subscribers.')

    return 1


def notify_subcribers(bot, update):
    subs = Subscriber.objects.all()
    message = update.message.text
    for sub in subs:
        bot.send_message(chat_id=sub.id, text=message)

    update.message.reply_text(f'Notification was sent to all {subs.count()} active subscribers.')


notify_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Send notification'), notify_claim)],
    states={
        1: [MessageHandler(Filters.text, notify_subcribers)],
    },
    fallbacks=[],
)
