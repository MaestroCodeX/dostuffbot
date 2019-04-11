from telegram import LabeledPrice
from telegram.ext import CallbackQueryHandler

import env
from main import texts, keyboards
from main.models import Faq


def help(bot, update):
    ''' Help section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=texts.HELP, reply_markup=keyboards.HELP_M, parse_mode='MARKDOWN')


def about(bot, update):
    ''' About section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=texts.ABOUT, reply_markup=keyboards.ABOUT_M)


def faq(bot, update):
    ''' FAQs section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(
        text=texts.FAQ,
        reply_markup=keyboards.faq_keyboard_markup(),
        parse_mode='MARKDOWN',
    )


def faq_by_id(bot, update):
    '''
    Handler selected faq with inline keyboard.
    Send full question, answer and propose to rate the issue.
    '''
    query = update.callback_query
    faq_id = query.data.split('__')[1]
    faq = Faq.objects.get(id=faq_id)
    query.edit_message_text(text=texts.FAQ_ID(faq), reply_markup=keyboards.faq_id_markup(faq), parse_mode='MARKDOWN')


def donate(bot, update):
    ''' Donate section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=texts.DONATE, reply_markup=keyboards.DONATE_M)


def donate_custom(bot, update):
    ''' Donate with custome amount section handler method called with inline keyboard '''
    query = update.callback_query
    query.edit_message_text(text=texts.DONATE_CUSTOM(0), reply_markup=keyboards.DONATE_CUSTOM_M)


def donate_add(bot, update):
    ''' Handle buttons on the custom donate amount keyboard. '''
    query = update.callback_query
    current_amount = int(query.message.text[:-1])
    add_number = int(query.data.split('__')[1])
    new_amount = current_amount * 10 + add_number
    query.edit_message_text(text=texts.DONATE_CUSTOM(new_amount), reply_markup=keyboards.DONATE_CUSTOM_M)


def donate_erase(bot, update):
    ''' Handle erase button on the custom donate amount keyboard. '''
    query = update.callback_query
    current_amount = int(query.message.text[:-1])
    new_amount = current_amount // 10
    query.edit_message_text(text=texts.DONATE_CUSTOM(new_amount), reply_markup=keyboards.DONATE_CUSTOM_M)


def donate_submit(bot, update):
    ''' Handle submit button on the custom donate amount keyboard. '''
    query = update.callback_query
    chat_id = query.message.chat_id
    amount = int(query.message.text[:-1])

    send_invoice(bot, chat_id, amount)


def donate_predefined(bot, update):
    ''' Handle predefined amount button and send a payment invoice. '''
    query = update.callback_query
    chat_id = query.message.chat_id
    amount = int(query.data.split('__')[1])

    send_invoice(bot, chat_id, amount)


def send_invoice(bot, chat_id, amount):
    ''' Send invoice with the given amount to the given chat. '''
    title = 'Payment Invoice'
    description = 'Support Dostuffbot 🤖.'
    payload = 'Support-Donate'
    provider_token = env.PAYMENT_TOKEN
    start_parameter = 'support-payment'
    currency = 'USD'

    # price * 100 so as to include 2 d.p.
    prices = [LabeledPrice('Support', amount * 100)]

    bot.send_invoice(
        chat_id, title, description, payload, provider_token, start_parameter, currency, prices
    )


help_handler = CallbackQueryHandler(help, pattern='help')
about_handler = CallbackQueryHandler(about, pattern='about')
faq_handler = CallbackQueryHandler(faq, pattern='^faq$')
faq_by_id_handler = CallbackQueryHandler(faq_by_id, pattern=r'^faq__\d*$')
donate_handler = CallbackQueryHandler(donate, pattern='^donate$')
donate_custom_handler = CallbackQueryHandler(donate_custom, pattern='donate_custom')
donate_add_handler = CallbackQueryHandler(donate_add, pattern=r'donate_add__\d?')
donate_erase_handler = CallbackQueryHandler(donate_erase, pattern=r'donate_erase')
donate_submit_handler = CallbackQueryHandler(donate_submit, pattern=r'donate_submit')
donate_predefined_handler = CallbackQueryHandler(donate_predefined, pattern=r'^donate__\d*$')
