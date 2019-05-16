import emoji


def build_deeplink(bot_name: str, parametr: str = None) -> str:
    link = 'https://t.me/' + bot_name
    if parametr:
        link += '?start=' + parametr
    return link


def get_telegram_user_from_update(update):
    if update.effective_user:
        return update.effective_user
    elif update.channel_post:
        return update.channel_post.from_user


def get_fullname(user):
    if user.username:
        return '@' + user.username
    fullname = user.first_name
    if user.last_name:
        fullname += ' ' + user.last_name
    return fullname


def emojize(text):
    return emoji.emojize(text, use_aliases=True)
