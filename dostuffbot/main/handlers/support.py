from telegram import LabeledPrice
from telegram.ext import CallbackQueryHandler

import env
from main import texts, keyboards
from main.models import Faq, FaqRate, User


def help(update, context):
    """ Help section handler method called with inline keyboard """
    query = update.callback_query
    query.edit_message_text(text=texts.HELP, reply_markup=keyboards.HELP_M, parse_mode='MARKDOWN')


def about(update, context):
    """ About section handler method called with inline keyboard """
    query = update.callback_query
    query.edit_message_text(text=texts.ABOUT, reply_markup=keyboards.ABOUT_M)


def faq(update, context):
    """ FAQs section handler method called with inline keyboard """
    query = update.callback_query
    queryset = Faq.objects.all()
    query.edit_message_text(
        text=texts.FAQ,
        reply_markup=keyboards.faq_keyboard_markup(queryset),
        parse_mode='MARKDOWN',
    )


def faq_by_id(update, context):
    """
    Handler selected faq with inline keyboard.
    Send full question, answer and propose to rate the issue.
    """
    query = update.callback_query
    faq_id = query.data.split('__')[1]
    faq = Faq.objects.get(id=faq_id)

    try:
        rate = FaqRate.objects.get(user__id=query.from_user.id)
        is_positive = rate.is_positive
    except FaqRate.DoesNotExist:
        is_positive = None
    text = texts.faq_id(faq)
    markup = keyboards.faq_id_markup(faq, vote=is_positive)
    query.edit_message_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')


def faq_rate(update, context):
    """
    Handler selected faq with inline keyboard.
    Send full question, answer and propose to rate the issue.
    """
    query = update.callback_query
    user = User.objects.get(id=query.from_user.id)
    faq_id = query.data.split('__')[1]
    faq = Faq.objects.get(id=faq_id)
    is_positive = '_up_' in query.data
    try:
        rate = FaqRate.objects.get(user=user, faq=faq)
        rate.is_positive = is_positive
        rate.save()
    except FaqRate.DoesNotExist:
        FaqRate.objects.create(user=user, faq=faq, is_positive=is_positive)

    text = texts.faq_id(faq)
    markup = keyboards.faq_id_markup(faq, vote=is_positive)
    query.edit_message_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')


def donate(update, context):
    """ Donate section handler method called with inline keyboard """
    query = update.callback_query
    query.edit_message_text(text=texts.DONATE, reply_markup=keyboards.DONATE_M)


def donate_custom(update, context):
    """ Donate with custome amount section handler method called with inline keyboard """
    query = update.callback_query
    query.edit_message_text(text=texts.donate_custom(0), reply_markup=keyboards.DONATE_CUSTOM_M)


def donate_add(update, context):
    """ Handle buttons on the custom donate amount keyboard. """
    query = update.callback_query
    current_amount = int(query.message.text[:-1])
    add_number = int(query.data.split('__')[1])
    new_amount = current_amount * 10 + add_number
    query.edit_message_text(text=texts.donate_custom(new_amount), reply_markup=keyboards.DONATE_CUSTOM_M)


def donate_erase(update, context):
    """ Handle erase button on the custom donate amount keyboard. """
    query = update.callback_query
    current_amount = int(query.message.text[:-1])
    new_amount = current_amount // 10
    query.edit_message_text(text=texts.donate_custom(new_amount), reply_markup=keyboards.DONATE_CUSTOM_M)


def donate_submit(update, context):
    """ Handle submit button on the custom donate amount keyboard. """
    query = update.callback_query
    chat_id = query.message.chat_id
    amount = int(query.message.text[:-1])

    send_invoice(context, chat_id, amount)


def donate_predefined(update, context):
    """ Handle predefined amount button and send a payment invoice. """
    query = update.callback_query
    chat_id = query.message.chat_id
    amount = int(query.data.split('__')[1])

    send_invoice(context, chat_id, amount)


def send_invoice(context, chat_id, amount):
    """ Send invoice with the given amount to the given chat. """
    title = 'Payment Invoice'
    description = 'Support Dostuffbot 🤖.'
    payload = 'Support-Donate'
    provider_token = env.PAYMENT_TOKEN
    start_parameter = 'support-payment'
    currency = 'USD'

    # price * 100 so as to include 2 d.p.
    prices = [LabeledPrice('Support', amount * 100)]

    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, start_parameter, currency, prices
    )


help_handler = CallbackQueryHandler(help, pattern='help')
about_handler = CallbackQueryHandler(about, pattern='about')
faq_handler = CallbackQueryHandler(faq, pattern='^faq$')
faq_by_id_handler = CallbackQueryHandler(faq_by_id, pattern=r'^faq__\d*$')
faq_rate_handler = CallbackQueryHandler(faq_rate, pattern=r'^faq_rate_(up|down)__\d*$')
donate_handler = CallbackQueryHandler(donate, pattern='^donate$')
donate_custom_handler = CallbackQueryHandler(donate_custom, pattern='donate_custom')
donate_add_handler = CallbackQueryHandler(donate_add, pattern=r'donate_add__\d?')
donate_erase_handler = CallbackQueryHandler(donate_erase, pattern=r'donate_erase')
donate_submit_handler = CallbackQueryHandler(donate_submit, pattern=r'donate_submit')
donate_predefined_handler = CallbackQueryHandler(donate_predefined, pattern=r'^donate__\d*$')
