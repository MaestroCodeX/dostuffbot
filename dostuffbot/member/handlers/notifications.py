from member import texts, keyboards, states
from member.handlers import start
from member.middleware import middleware


@middleware
def notify_claim(update, context):
    """ Callback function when user wants to send message to his subscribers. """

    subs_count = context.bot.db_bot.subscriber_set.count()
    update.message.reply_text(
        ('Okay, send a message that you want to share with your subscribers.\n\n'
            f'The message will be immediately sent to all {subs_count} subscribers.'),
        reply_markup=keyboards.back_markup('start'),
    )

    return states.SEND_NOTIFY_MESSAGE


@middleware
def notify_subcribers(update, context):
    """ Callback function when user sent message with a text for a notification.
    Send a message to all subscribers and return user to start menu. """

    if len(update.message.text) >= 500:
        update.message.reply_text(
            'The message is too long. Divide it into several parts. The maximum length is 500 characters.')
        return states.SEND_NOTIFY_MESSAGE

    subs = context.bot.db_bot.subscriber_set.all()
    notify_subscribers_with_text(context.bot, subs, update.message)
    start.start(update, context)

    return states.START_MENU


def notify_subscribers_with_text(bot, subs, message):
    """ Send notification to user from queryset.
    Also keep editing a message sending status with counter for admin. """
    subs_count = subs.count()
    text_status = texts.message_mailing_status(0, subs_count)
    status_message = message.reply_text(text_status)
    for i, sub in enumerate(subs, 1):
        try:
            bot.send_message(chat_id=sub.id, text=message.text)
        except Exception:
            pass
        if i % 5 == 0:
            text_status = texts.message_mailing_status(i, subs_count)
            status_message.edit_text(text_status)
    status_message.edit_text(texts.notification_sent(subs_count, subs_count))
