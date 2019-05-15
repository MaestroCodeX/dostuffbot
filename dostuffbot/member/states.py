from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from core.handlers import ignore
from member import states, texts
from member.handlers import commands, command_addition, notifications, start
from member.utils import to_filter_regex

STATE_INDEX = 0


def state():
    global STATE_INDEX
    STATE_INDEX += 1
    return STATE_INDEX


START_MENU = state()
SETTINGS = state()
COMMAND_MENU = state()
SEND_CALLER = state()
SEND_MESSAGE = state()
CHOOSE_COMMAND_OPTION = state()
DELETE_CONFIRM = state()
BACK_START = state()


base_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start.start)],
    states={
        states.START_MENU: [
            MessageHandler(to_filter_regex(texts.COMMANDS), commands.commands_list),
            MessageHandler(to_filter_regex(texts.SEND_NOTIFICATION), notifications.notify_claim),
        ],
        states.COMMAND_MENU: [
            MessageHandler(Filters.command, commands.command_menu),
            MessageHandler(to_filter_regex(texts.ADD_COMMAND), command_addition.command_add),
            MessageHandler(Filters.regex(texts.back_text('start')), start.start),
        ],
        states.CHOOSE_COMMAND_OPTION: [
            MessageHandler(to_filter_regex(texts.DELETE_COMMAND), commands.command_delete),
            MessageHandler(to_filter_regex(texts.SHOW_ANSWER), commands.command_show_answer),
            MessageHandler(to_filter_regex(texts.back_text('commands list')), commands.commands_list),
        ],
        states.DELETE_CONFIRM: [
            MessageHandler(to_filter_regex(texts.DELETE_COMMAND_CONFIRM), commands.command_delete_confirm),
            MessageHandler(Filters.all, commands.command_menu),
        ],
    },
    fallbacks=[MessageHandler(Filters.all, ignore)],
)
