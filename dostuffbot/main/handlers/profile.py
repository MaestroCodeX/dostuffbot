from telegram.ext import CallbackQueryHandler

from main import texts, keyboards
from main.utils import call_bot_regex, get_bot_from_call


def bot_profile(bot, update):
    query = update.callback_query

    bot = get_bot_from_call(query.data)

    query.edit_message_text(
        text=texts.PROFILE(bot),
        reply_markup=keyboards.profile_m(bot)
    )


bot_profile_handler = CallbackQueryHandler(bot_profile, call_bot_regex('profile'))
