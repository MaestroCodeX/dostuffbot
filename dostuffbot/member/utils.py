from django.utils import translation

from member.models import BotAdmin, Bot


def get_me_from_db(bot):
    my_bot = bot.get_me()
    return Bot.objects.get(id=my_bot.id)


def admin_only(func):
    def func_wrapper(bot, update):
        user_id = update.effective_user.id
        if not BotAdmin.objects.filter(user__id=user_id).exists():
            return

        return func(bot, update)

    return func_wrapper


def activate_language(bot, update):
    lang = update.effective_user.language_code
    translation.activate(lang)


MIDDLEWARES = [
    activate_language,
]


def middleware(func):
    def func_wrapper(bot, update):
        for middleware in MIDDLEWARES:
            middleware(bot, update)
        return func(bot, update)

    return func_wrapper
