from django.conf import settings as django_settings
from main.utils import e


def add_header(text):
    return text  # HEADER + text


def donate_custom(n):
    return f'{n}$'


def delete_bot(bot):
    return f'You are about to delete your bot ***I{bot.name}*** {bot.full_username}. Is that correct?'


def bot_profile(username):
    return f'***Bot Name***: {username}\n\nSelect what you want to do:'


def faq_id(faq):
    rates_count = faq.rates.filter(is_positive=True).count()
    return add_header(e(f'***{faq.question}***\n\n{faq.answer}\n\n:thumbsup: ({rates_count})\nWas it helpful?'))


def bot_settings(bot):
    return 'Settings.'


def settings(user):
    lang = dict(django_settings.LANGUAGES).get(user.lang, 'English')
    return add_header(f'***Language***: {lang}')


HEADER = 'Dostuffbot 🤖\n\n'
START = add_header((
    '***Dostuffbot*** is created to help you build your own bots without any coding. '
    'It\'s simple and absolutely free for use.'
))
BOT_CONNECT = e(add_header((
    'To connect your bot:\n\n'
    ':small_blue_diamond: Go to @BotFather.\n'
    ':small_blue_diamond: Send /addbot and set a name for it.\n'
    ':small_blue_diamond: Copy a token you get if bot is created.\n'
    ':small_blue_diamond: Return to me and send it.\n\n'
    'Example of the token: `987865432:AAA-50DXLLPYEl1TDbnPYElDimH9CouAhfXLLM`'
)))
TOKEN_INVALID = BOT_CONNECT + e(
    '\n\nThe token is invalid :heavy_exclamation_mark:'
)
BOT_CONNECTED = e(
    'Your bot was succesfully added to the system :bear:\n\n'
)
HELP = add_header((
    'I am a bot builder that can help you create your bots without any boring coding.\n'
    'I try to customize every bot for their needs as much as possible.\n\n'
    '***To start*** go to menu and add your first bot. Then follow the inctructions to manage it.\n\n'
    'If you still have any question feel free to check out FAQs '
    'or contact us at @dostuffsupportbot.'
))
ABOUT = add_header((
    'I am bot who lives together with my creator @serhii_beznisko. '
    'My creator is a typical student who likes to code and drink enormous cups of tea.\n\n'
    'If you like me you can support my creator by donating a small amout of money. '
    'He will pay servers and buy better computers so I can work even faster!\n\n'
    'Feel free to contact us at @dostuffsupportbot.'
))
DONATE = add_header(
    'Your help is significant. Select an amount you want to donate or hit custom.'
)
CHOOSE_BOT = add_header('Choose a bot from the list below:')
NO_BOTS = add_header('You haven\'t connected any bots yet.')
BOT_DELETED = 'Bot got forgotten forever.'
SEARCHING_BOT = add_header('Searching your bot...')
FAQ = add_header((
    'Here are the most common questions.\n\n'
    '***Not what you\'re looking for?*** Try asking the `Help Community`'
))
EDIT_LANG = add_header('Choose a language from the list below:')
