import re

from telegram.ext import MessageHandler, Filters
from django.conf import settings

from member.models import BotAdmin, Command, Subscriber, Bot


def admin_only(func):
    def func_wrapper(bot, update):
        user_id = update.effective_user.id
        if not BotAdmin.objects.filter(bot=bot.db_bot, user__id=user_id).exists():
            return

        return func(bot, update)

    return func_wrapper


def call_command(bot_id: int, command: str) -> str:
    return settings.COMMAND_CALL_PREFIX + str(bot_id) + '__' + command


def call_command_regex(command) -> str:
    return '^' + settings.COMMAND_CALL_PREFIX + r'\d*__' + command + '$'


def get_command_id_from_call(call):
    r = re.search(settings.COMMAND_ID_REGEX, call)
    if not r:
        raise ValueError('Could not parse command ID from call.')
    return r.groups()[0]


def get_command_from_call(bot, call):
    command_id = get_command_id_from_call(call)
    try:
        command = Command.objects.get(id=command_id, bot=bot.db_bot)
    except Command.DoesNotExist:
        raise ValueError('Could not find a command with given ID from call.')

    return command


def get_handler(command):
    def handler(bot, update):
        Subscriber.objects.get_or_create(id=update.effective_user.id, bot=bot.db_bot)
        messages = command.command_messages.all()
        for message in messages:
            update.message.reply_text(
                message.text,
                parse_mode='MARKDOWN',
            )

    return handler


def command_handler(command):
    return MessageHandler(Filters.regex(f'^{command.caller}$'), get_handler(command))
