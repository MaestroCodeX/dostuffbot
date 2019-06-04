from telegram.ext import MessageHandler, Filters
from member.models import Subscriber
from member.permissions import subscriber_only


def get_handler(command):
    """ Return a function for the given command.
    It will be called every time the user calls given command.
    Do not answer if the user is the admin. """

    @subscriber_only
    def handler(update, context):
        Subscriber.objects.get_or_create(id=update.effective_user.id, bot=context.bot.db_bot)
        command.reply_to(update.message)

    return handler


def get_command_handler(command):
    """ Return a MessageHandler for the custom command.
    Additionally assign id of the command to handler
    so it can be removed when command isntance is deleted. """

    handler = MessageHandler(to_filter_regex(command.caller), get_handler(command))
    handler.id = command.id
    return handler


def to_filter_regex(text):
    """ Return a filter with given text wrapped with ^ and $
    so that regex will match exactly this text. """

    return Filters.regex(f'^{text}$')
