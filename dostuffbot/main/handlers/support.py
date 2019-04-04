from telegram import ParseMode
from telegram.ext import CallbackQueryHandler

from main.keyboards import help_markup, about_markup
from main.texts import help_text, about_text


def help(bot, update):
    ''' Help section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=help_text, reply_markup=help_markup, parse_mode=ParseMode.MARKDOWN)


def about(bot, update):
    ''' About section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=about_text, reply_markup=about_markup)


help_handler = CallbackQueryHandler(help, pattern='help')
about_handler = CallbackQueryHandler(about, pattern='about')
