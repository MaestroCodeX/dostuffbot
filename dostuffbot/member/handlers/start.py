from telegram.ext import Filters, CommandHandler, MessageHandler, Dispatcher

from core.enums import DeepCommand
from member import texts, keyboards
from member.handlers import commands
from member.models import Subscriber
from member.utils import admin_only, middleware


@admin_only
@middleware
def start(bot, update):
    dispatcher = Dispatcher.get_instance()
    db_bot = dispatcher.db_bot

    # Subscribe every user that sends /start to the bot
    Subscriber.objects.get_or_create(id=update.effective_user.id, bot=db_bot)

    args = update.message.text.split()
    if len(args) > 1:
        handle_start_command(bot, update, args[1])
        # break further execution as soon as user did't want to send start command
        return

    update.message.reply_text(
        texts.START,
        reply_markup=keyboards.START_M,
        parse_mode='MARKDOWN',
    )


def handle_start_command(bot, update, command):
    if command == DeepCommand.COMMANDS:
        commands.commands(bot, update)
    elif command == DeepCommand.NOTIFY:
        update.message.text = 'Send notification'
        Dispatcher.get_instance().process_update(update)


start_handler = CommandHandler('start', start)
menu_handler = MessageHandler(Filters.regex('Menu'), start)
