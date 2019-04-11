from telegram.ext import CallbackQueryHandler

from main import texts, keyboards
from main.models import User
from main.utils import call_bot_regex, get_bot_from_call


def my_bots(bot, update):
    ''' Show user bots list with inline keyboard '''
    query = update.callback_query
    user = User.objects.get(id=query.from_user.id)
    bots = user.bot_set.all()

    if bots.count():
        text = texts.CHOOSE_BOT
        markup = keyboards.my_bots_m(bots)
    else:
        text = texts.NO_BOTS
        markup = keyboards.CONNECT_BOT_M

    query.answer()
    query.edit_message_text(text=text, reply_markup=markup)


def bot_profile(bot, update):
    ''' Show bot profile '''
    query = update.callback_query

    bot = get_bot_from_call(query.data)

    query.edit_message_text(
        text=texts.bot_profile(bot.name),
        reply_markup=keyboards.bot_profile_m(bot),
        parse_mode='MARKDOWN',
    )


def delete_bot(bot, update):
    query = update.callback_query

    bot = get_bot_from_call(query.data)
    text = texts.delete_bot(bot)
    markup = keyboards.confirm_deletion_markup(bot)

    query.edit_message_text(text=text, reply_markup=markup, parse_mode='MARKDOWN')


def delete_bot_confirm(bot, update):
    query = update.callback_query

    bot = get_bot_from_call(query.data)
    bot.delete()

    query.answer(texts.BOT_DELETED)
    my_bots(bot, update)


my_bots_handler = CallbackQueryHandler(my_bots, pattern='my_bots')
bot_profile_handler = CallbackQueryHandler(bot_profile, pattern=call_bot_regex('profile'))
delete_bot_handler = CallbackQueryHandler(delete_bot, pattern=call_bot_regex('delete'))
delete_bot_confirm_handler = CallbackQueryHandler(delete_bot_confirm, pattern=call_bot_regex('delete_confirm'))
