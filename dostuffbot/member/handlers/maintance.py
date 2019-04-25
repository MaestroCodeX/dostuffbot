from telegram.ext import ConversationHandler, CommandHandler

from member.handlers import start


def fallback(bot, update):
    start.start(bot, update)
    return ConversationHandler.END


fallback_handler = CommandHandler('start', fallback)
