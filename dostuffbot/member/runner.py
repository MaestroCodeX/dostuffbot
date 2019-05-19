import logging

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from django.conf import settings

from core import logger
from core.handlers import ignore
from member import states, texts
from member.handlers import commands, command_addition, command_edition, notifications, start, bot_settings
from member.utils import get_command_handler, to_filter_regex


base_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start.start)],
    states={
        states.START_MENU: [
            MessageHandler(to_filter_regex(texts.COMMANDS), commands.commands_list),
            MessageHandler(to_filter_regex(texts.SEND_NOTIFICATION), notifications.notify_claim),
            MessageHandler(to_filter_regex(texts.SETTINGS), bot_settings.settings),
        ],
        states.COMMAND_MENU: [
            MessageHandler(Filters.command, commands.command_menu),
            MessageHandler(to_filter_regex(texts.ADD_COMMAND), command_addition.command_add),
            MessageHandler(Filters.regex(texts.back_text('start')), start.start),
        ],
        states.CHOOSE_COMMAND_OPTION: [
            MessageHandler(to_filter_regex(texts.EDIT_COMMAND), command_edition.command_edit_caller),
            MessageHandler(to_filter_regex(texts.SHOW_ANSWER), commands.command_show_answer),
            MessageHandler(to_filter_regex(texts.DELETE_COMMAND), commands.command_delete),
            MessageHandler(to_filter_regex(texts.back_text('commands list')), commands.commands_list),
        ],
        states.DELETE_CONFIRM: [
            MessageHandler(to_filter_regex(texts.DELETE_COMMAND_CONFIRM), commands.command_delete_confirm),
            MessageHandler(Filters.all, commands.command_menu),
        ],
        states.SEND_NOTIFY_MESSAGE: [
            MessageHandler(to_filter_regex(texts.back_text('start')), start.start),
            MessageHandler(Filters.text, notifications.notify_subcribers),
        ],
        states.INPUT_CALLER: [
            MessageHandler(to_filter_regex(texts.back_text('command menu')), commands.commands_list),
            MessageHandler(Filters.command, command_addition.command_add_caller),
        ],
        states.INPUT_EDIT_CALLER: [
            MessageHandler(to_filter_regex(texts.back_text('command menu')), commands.commands_list),
            MessageHandler(Filters.command, command_edition.command_edit_caller_sent),
        ],
        states.SEND_MESSAGE: [
            MessageHandler(Filters.regex('Complete'), command_addition.command_add_complete),
            MessageHandler(Filters.regex('Cancel'), command_addition.command_add_cancel),
            MessageHandler(Filters.text, command_addition.command_add_text),
            MessageHandler(Filters.photo, command_addition.command_add_photo),
            MessageHandler(Filters.video, command_addition.command_add_video),
            MessageHandler(Filters.document, command_addition.command_add_document),
            MessageHandler(Filters.audio, command_addition.command_add_audio),
            MessageHandler(Filters.voice, command_addition.command_add_voice),
            MessageHandler(Filters.location, command_addition.command_add_location),
        ],
        states.BACK_START: [
            MessageHandler(Filters.regex(texts.back_text('start')), start.start),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)],
)

ADMIN_HANDLERS = [
    base_conversation,
]


def run_bot_with_handlers(instance):
    # Configure bot
    # my_persistence = PicklePersistence(filename='my_file')
    updater = Updater(instance.token, use_context=True)
    dp = updater.dispatcher
    dp.db_bot = instance
    dp.bot.db_bot = instance

    # Add handlers
    for handler in ADMIN_HANDLERS:
        dp.add_handler(handler, group=settings.ADMIN_HANDLER_GROUP)

    commands = instance.commands.all()
    for command in commands:
        handler = get_command_handler(command)
        dp.add_handler(handler, group=settings.DEFAULT_HANDLER_GROUP)

    # Log all errors
    dp.add_error_handler(logger.error)

    # TODO: Run bot in a new thread
    # Start bot
    updater.start_polling()
    logging.info('Bot is running.')
