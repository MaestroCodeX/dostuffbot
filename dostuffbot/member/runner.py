import logging

from telegram.ext import Updater
from django.conf import settings

from core import logger
from member.handlers import start, commands, notifications
from member.utils import command_handler

ADMIN_GROUP = 1
ADMIN_HANDLERS = [
    start.start_handler,
    start.start_command_handler,
    commands.commands_list_handler,
    commands.command_add_handler,
    commands.command_menu_handler,
    commands.command_delete_handler,
    commands.command_delete_confirm_handler,
    commands.command_edit_caller_handler,
    notifications.notify_handler,
]


def run_bot_with_handlers(instance):
    # Configure bot
    updater = Updater(instance.token)
    dp = updater.dispatcher
    dp.db_bot = instance
    dp.bot.db_bot = instance

    # Add handlers
    for handler in ADMIN_HANDLERS:
        dp.add_handler(handler, group=ADMIN_GROUP)

    commands = instance.commands.all()
    for command in commands:
        handler = command_handler(command)
        dp.add_handler(handler, group=settings.DEFAULT_HANDLER_GROUP)

    # Log all errors
    dp.add_error_handler(logger.error)

    # TODO: Run bot in a new thread
    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
