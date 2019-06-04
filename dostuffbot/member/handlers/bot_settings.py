from django.conf import settings as django_settings

from core.utils import build_deeplink
from main.utils import call_bot
from member import keyboards, states
from member.middleware import middleware


@middleware
def settings(update, context):
    """ Callback function when user sends /start or returns to main menu.
    It also handles start command with arguments from main bot. """

    db_bot = context.bot.db_bot
    settings_link = build_deeplink(django_settings.MAIN_BOT_NAME, call_bot(db_bot.id, 'profile'))
    update.message.reply_text(
        f'To manage {db_bot.name} settings go to its [profile]({settings_link}).',
        reply_markup=keyboards.start_markup(),
        parse_mode='MARKDOWN',
    )

    return states.START_MENU
