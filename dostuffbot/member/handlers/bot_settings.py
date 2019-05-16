from core.utils import build_deeplink
from main.utils import call_bot
from member import keyboards, states
from member.middleware import middleware


@middleware
def settings(update, context):
    """ Callback function when user sends /start or returns to main menu.
    It also handles start command with arguments from main bot. """

    db_bot = context.bot.db_bot
    settings_link = build_deeplink('Dostuffbot', call_bot(db_bot.id, 'profile'))
    update.message.reply_text(
        f'To manage {db_bot.name} settings of the bot go to his [profile]({settings_link}).',
        reply_markup=keyboards.back_markup('start'),
        parse_mode='MARKDOWN',
    )

    return states.BACK_START
