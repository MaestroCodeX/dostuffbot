from telegram.ext import Filters, MessageHandler

from member import texts, keyboards
from member.models import Command
from member.utils import admin_only


@admin_only
def commands(bot, update):
    commands = Command.objects.all()
    update.message.reply_text(
        texts.COMMANDS,
        reply_markup=keyboards.commands_keyboard(commands),
        parse_mode='MARKDOWN',
    )


commands_handler = MessageHandler(Filters.regex('Commands'), commands)
