import re

from django.conf import settings

from member.models import BotAdmin, Command


def admin_only(func):
    def func_wrapper(bot, update):
        user_id = update.effective_user.id
        if not BotAdmin.objects.filter(user__id=user_id).exists():
            return

        return func(bot, update)

    return func_wrapper


MIDDLEWARES = [
]


def middleware(func):
    def func_wrapper(bot, update):
        for middleware in MIDDLEWARES:
            middleware(bot, update)
        return func(bot, update)

    return func_wrapper


def call_command(bot_id: int, command: str) -> str:
    return settings.COMMAND_CALL_PREFIX + str(bot_id) + '__' + command


def call_command_regex(command) -> str:
    return '^' + settings.COMMAND_CALL_PREFIX + r'\d*__' + command + '$'


def get_command_from_call(call):
    print(call)
    r = re.search(settings.COMMAND_ID_REGEX, call)
    if not r:
        raise ValueError('Could not parse command ID from call.')

    command_id = r.groups()[0]
    try:
        command = Command.objects.get(id=command_id)
    except Command.DoesNotExist:
        raise ValueError('Could not find a command with given ID from call.')

    return command
