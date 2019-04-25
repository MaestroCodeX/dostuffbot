from telegram.ext import Filters, MessageHandler, ConversationHandler

from member import texts, keyboards
from member.handlers import maintance
from member.models import Command
from member.utils import admin_only, middleware


@admin_only
@middleware
def commands(bot, update):
    commands = Command.objects.all()
    update.message.reply_text(
        texts.COMMANDS,
        reply_markup=keyboards.commands_markup(commands),
        parse_mode='MARKDOWN',
    )

    return 1


@admin_only
@middleware
def command_menu(bot, update):
    command = update.message.text[1:]
    command = Command.objects.get(text=command)
    update.message.reply_text(
        texts.command_menu(command),
        reply_markup=keyboards.command_menu_markup(command),
        parse_mode='MARKDOWN',
    )

    return 2


@admin_only
@middleware
def edit_command(bot, update):
    update.message.reply_text(
        texts.edit_command(command),
        reply_markup=keyboards.command_menu_markup(command),
        parse_mode='MARKDOWN',
    )


commands_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('Commands'), commands)],
    states={
        1: [MessageHandler(Filters.regex('/.*'), command_menu)],
    },
    fallbacks=[maintance.fallback_handler],
)
