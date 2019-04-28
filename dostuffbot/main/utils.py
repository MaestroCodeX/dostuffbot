import re
import emoji
import logging

from telegram import Message
from django.conf import settings

# from main.constants import BOT_CALL_PREFIX, BOT_ID_REGEX
from main.models import User
from member.models import Bot


def emojize(text):
    return emoji.emojize(text, use_aliases=True)


def get_or_create_user(message: Message) -> User:
    from_user = message.from_user
    try:
        user = User.objects.get(id=from_user.id)
    except User.DoesNotExist:
        user = User.objects.create(
            id=from_user.id,
            first_name=from_user.first_name,
            last_name=from_user.last_name,
            username=from_user.username,
            lang=from_user.language_code,
            is_bot=from_user.is_bot,
        )
    return user


def build_deeplink(bot_name: str, parametr: str = None) -> str:
    link = 'https://t.me/' + bot_name
    if parametr:
        link += '?start=' + parametr
    return link


def call_bot(bot_id: int, command: str) -> str:
    return settings.BOT_CALL_PREFIX + str(bot_id) + '__' + command


def call_bot_regex(command) -> str:
    return '^' + settings.BOT_CALL_PREFIX + r'\d*__' + command + '$'


def get_bot_from_call(call: str, caller: int) -> Bot:
    r = re.search(settings.BOT_ID_REGEX, call)
    if not r:
        raise ValueError('Could not parse bot ID from call.')

    bot_id = r.groups()[0]
    try:
        bot = Bot.objects.get(id=bot_id, owner__id=caller)
    except Bot.DoesNotExist:
        raise ValueError('Could not find a bot with given ID from call.')

    return bot


def log_exception(func):
    def func_wrapper(bot, update):
        try:
            return func(bot, update)
        except Exception as e:
            logging.error(e)

    return func_wrapper
