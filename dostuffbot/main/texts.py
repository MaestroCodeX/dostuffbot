from main.utils import e


def add_header(text):
    return HEADER + text


HEADER = 'Do stuff bot 🤖\n\n'
START = add_header((
    '***Dostuffbot*** is created to help you build your own bots without any coding.'
    'It\'s simple and absolutely free for use.'
))
BOT_CONNECT = e(add_header((
    'To connect your bot:\n\n'
    ':small_blue_diamond: Go to @BotFather.\n'
    ':small_blue_diamond: Send /addbot and set a name for it.\n'
    ':small_blue_diamond: Copy a token you get if bot is created.\n'
    ':small_blue_diamond: Return to me and send it.\n\n'
    'Example of the token: ```987865432:AAA-50DXLLPYEl1TDbnPYElDimH9CouAhfXLLM```'
)))
TOKEN_INVALID = BOT_CONNECT + e(
    '\n\nThe token is invalid :heavy_exclamation_mark:'
)
BOT_CONNECTED = e(
    'Your bot was succesfully added to the system :bear:'
)
HELP = add_header((
    'I am a bot builder that can help you create your bots without any boring coding.\n'
    'I try to customize every bot for their needs as much as possible.\n\n'
    '***To start*** go to menu and add your first bot. Then follow the inctructions to manage it.\n\n'
    'If you still have any question feel free to check out frequently asked questions (FAQs) '
    'or contact us at @dostuffsupportbot.'
))
ABOUT = add_header((
    'I am bot who lives together with my creator @serhii_beznisko. '
    'My creator is a typical student who likes to code and drink enormous cups of tea.\n\n'
    'If you like me you can support my creator by donating a small amout of money. '
    'He will pay servers and buy better computers so I can work even faster!\n\n'
    'Feel free to contact him at @dostuffsupportbot.'
))
