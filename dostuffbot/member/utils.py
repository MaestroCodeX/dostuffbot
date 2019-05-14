from telegram.ext import MessageHandler, Filters
from member.models import BotAdmin, Command, Subscriber


def admin_only(func):
    def func_wrapper(update, context):
        user_id = update.effective_user.id
        if not BotAdmin.objects.filter(bot=context.bot.db_bot, user__id=user_id).exists():
            return

        return func(update, context)

    return func_wrapper


def get_command_from_context(context):
    command_id = context.chat_data.get('cmd_id')
    if not command_id:
        raise ValueError('No command ID found in context.')
    db_bot = context.bot.db_bot
    try:
        return Command.objects.get(bot=db_bot, id=command_id)
    except Command.DoesNotExist:
        raise ValueError('Could not find a command with given ID from call.')


def get_handler(command):
    def handler(update, context):
        Subscriber.objects.get_or_create(id=update.effective_user.id, bot=context.bot.db_bot)
        command.reply_to(update.message)

    return handler


def get_command_handler(command):
    return MessageHandler(Filters.regex(f'^{command.caller}$'), get_handler(command))


def to_filter_regex(text):
    return Filters.regex(f'^{text}$')


def back_to_message_handler(pattern, callback):
    pass
