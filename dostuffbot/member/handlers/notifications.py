from member import texts, keyboards, states
from member.handlers import start
from member.middleware import middleware
from member.models import Subscriber


@middleware
def notify_claim(update, context):
    """ Callback function when user wants to send message to his subscribers. """

    update.message.reply_text(
        'Send me a message that you want to share with your subscribers.',
        reply_markup=keyboards.back_markup('start'),
    )

    return states.SEND_NOTIFY_MESSAGE


@middleware
def notify_subcribers(update, context):
    """ Callback function when user sent message with a text for a notification.
    Send a message to all subscribers and return user to start menu. """

    subs = Subscriber.objects.filter(bot=context.bot.db_bot)
    notify_subscribers_with_text(context.bot, subs, update.message)
    start.start(update, context)

    return states.START_MENU


def notify_subscribers_with_text(bot, subs, message):
    """ Send notification to user from queryset.
    Also keep editing a message sending status with counter for admin. """

    text_status = texts.message_mailing_status(0, subs.count())
    status_message = message.reply_text(text_status)
    for i, sub in enumerate(subs, 1):
        bot.send_message(chat_id=sub.id, text=message.text)
        text_status = texts.message_mailing_status(i, subs.count())
        status_message.edit_text(text_status)
    status_message.edit_text(texts.notification_sent(subs.count(), subs.count()))
