from telegram.ext import MessageHandler, Filters
from member.models import BotAdmin, Subscriber


def admin_only(func):
    def func_wrapper(update, context):
        user_id = update.effective_user.id
        if not BotAdmin.objects.filter(bot=context.bot.db_bot, user__id=user_id).exists():
            return
        return func(update, context)
    return func_wrapper


def subscriber_only(func):
    def func_wrapper(update, context):
        user_id = update.effective_user.id
        if BotAdmin.objects.filter(bot=context.bot.db_bot, user__id=user_id).exists():
            return
        return func(update, context)
    return func_wrapper


def get_handler(command):
    @subscriber_only
    def handler(update, context):
        Subscriber.objects.get_or_create(id=update.effective_user.id, bot=context.bot.db_bot)
        command.reply_to(update.message)

    return handler


def get_command_handler(command):
    handler = MessageHandler(to_filter_regex(command.caller), get_handler(command))
    handler.id = command.id
    return handler


def to_filter_regex(text):
    return Filters.regex(f'^{text}$')
