from django.conf import settings as django_settings
from django.utils.translation import gettext as _
from main.utils import e


def add_header(text):
    return text


def donate_custom(n):
    return f'{n}$'


def delete_bot(bot):
    text = _('You are about to delete your bot ***{name}*** {username}. Is that correct?')
    return text.format(name=bot.name, username=bot.full_username)


def bot_profile(username):
    text = _('***Bot Name***: {}\n\nSelect what you want to do:')
    return text.format(username)


def faq_id(faq):
    rates_count = faq.rates.filter(is_positive=True).count()
    text = add_header(e(_('***{q}***\n\n{a}\n\n:thumbsup: ({rates_count})\nWas it helpful?')))
    return text.format(q=faq.question, a=faq.answer, rates_count=rates_count)


def bot_settings(bot):
    return _('Settings.')


def settings(user):
    lang = dict(django_settings.LANGUAGES).get(user.lang, 'English')
    text = add_header(_('***Language***: {}'))
    return text.format(lang)


HEADER = 'Dostuffbot 🤖\n\n'
START = add_header((
    '***Dostuffbot*** is created to help you build your own bots without any coding. '
    'It\'s simple and absolutely free for use.'
))
BOT_CONNECT = add_header(e(_('main_bot_connect')))
TOKEN_INVALID = BOT_CONNECT + '\n\n' + e(_('main_token_invalid'))
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
