import logging

from telegram.ext import Updater, Filters, MessageHandler

from core import logger
from member.handlers import start, commands, notifications
from member.models import Subscriber, Bot

ADMIN_GROUP = 1
ADMIN_HANDLERS = [
    start.start_handler,
    start.menu_handler,
    commands.commands_handler,
    notifications.notify_handler,
]


def get_handler(command):
    def handler(bot, update):
        user_bot = bot.get_me()
        my_bot = Bot.objects.get(id=user_bot.id)
        Subscriber.objects.get_or_create(id=update.effective_user.id, bot=my_bot)
        update.message.reply_text(
            command.content,
            parse_mode='MARKDOWN',
        )

    return handler


def command_handler(command):
    return MessageHandler(Filters.regex(f'^{command.text}$'), get_handler(command))


def run_bot_with_handlers(instance):
    # Configure bot
    updater = Updater(instance.token)
    dp = updater.dispatcher
    dp.db_bot = instance

    # Add handlers
    for handler in ADMIN_HANDLERS:
        dp.add_handler(handler, group=ADMIN_GROUP)

    commands = instance.commands.all()
    for command in commands:
        handler = command_handler(command)
        dp.add_handler(handler)

    # Log all errors
    dp.add_error_handler(logger.error)

    # TODO: Run bot in a new thread
    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
