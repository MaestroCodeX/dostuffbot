from telegram.ext import Filters, MessageHandler

from core.utils import get_user_from_request


def unknown(update, context):
    """ Default handler when no other handlers worked. Just delete the message. """
    get_user_from_request(update, context).not_on_top()


def idle(update, context):
    pass


unknown_handler = MessageHandler(Filters.all, unknown)
