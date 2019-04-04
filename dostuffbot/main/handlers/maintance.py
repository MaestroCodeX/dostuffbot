from telegram.ext import Filters, MessageHandler


def unknown(bot, update):
    ''' Default handler when no other handlers worked. Just delete the message. '''
    update.message.delete()


unknown_handler = MessageHandler(Filters.all, unknown)
