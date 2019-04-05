from telegram.ext import CallbackQueryHandler

from main.keyboards import get_profile_markup
from main.texts import get_profile_text
from main.utils import call_bot_regex, get_bot_from_call


def bot_profile(bot, update):
    query = update.callback_query

    bot = get_bot_from_call(query.data)

    query.edit_message_text(
        text=get_profile_text(bot),
        reply_markup=get_profile_markup(bot)
    )


bot_profile_handler = CallbackQueryHandler(bot_profile, call_bot_regex('profile'))
