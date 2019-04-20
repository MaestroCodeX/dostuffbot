from telegram.ext import Filters, MessageHandler, ConversationHandler, CommandHandler

from member import texts, keyboards
from member.models import Command
from member.utils import admin_only, middleware


@admin_only
@middleware
def commands(bot, update):
    commands = Command.objects.all()
    update.message.reply_text(
        texts.COMMANDS,
        reply_markup=keyboards.commands_keyboard(commands),
        parse_mode='MARKDOWN',
    )

    return 1


@admin_only
@middleware
def command_menu(bot, update):
    command = update.message.text[1:]
    command = Command.objects.get(text=command)
    update.message.reply_text(
        texts.COMMANDS,
        reply_markup=keyboards.command_menu(command),
        parse_mode='MARKDOWN',
    )


commands_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Commands'), commands)],
    states={
        1: [MessageHandler(Filters.regex('/.*'), command_menu)],
    },
    fallbacks=[],
)
