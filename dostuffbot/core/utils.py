import emoji

from main.models import User


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


def escape_markdown(text):
    return (text.replace("_", "\\_")
            .replace("*", "\\*")
            .replace("[", "\\[")
            .replace("`", "\\`"))


def emojize(text):
    return emoji.emojize(text, use_aliases=True)


def get_user_from_request(update, context):
    user = context.chat_data.get('user')
    if not user:
        try:
            user = User.objects.get(id=update.effective_user.id)
        except User.DoesNotExist:
            from_user = update.effective_user
            user = User.objects.create(
                id=from_user.id,
                first_name=from_user.first_name,
                last_name=from_user.last_name,
                username=from_user.username,
                lang=from_user.language_code,
                is_bot=from_user.is_bot,
            )
        context.chat_data['user'] = user

    return user
