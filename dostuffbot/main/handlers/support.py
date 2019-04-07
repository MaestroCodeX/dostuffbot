from telegram import ParseMode
from telegram.ext import CallbackQueryHandler

from main import texts, keyboards


def help(bot, update):
    ''' Help section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=texts.HELP, reply_markup=keyboards.HELP_M, parse_mode=ParseMode.MARKDOWN)


def about(bot, update):
    ''' About section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=texts.ABOUT, reply_markup=keyboards.ABOUT_M)


def donate(bot, update):
    ''' Donate section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=texts.DONATE, reply_markup=keyboards.DONATE_M)


help_handler = CallbackQueryHandler(help, pattern='help')
about_handler = CallbackQueryHandler(about, pattern='about')
