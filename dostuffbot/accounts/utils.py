from telegram import User as TelegramUser

from accounts.models import User


def get_user_from_message(message):
    from_user = message.from_user
    try:
        user = User.objects.get(id=from_user.id)
    except User.DoesNotExist:
        user = User.objects.create(
            id=from_user.id,
            first_name=from_user.first_name,
            last_name=from_user.last_name,
            username=from_user.username,
            lang=from_user.language_code,
            is_bot=from_user.is_bot,
        )

    return user


def get_telegram_user(user):
    t_user = TelegramUser(
        id=user.id,
        is_bot=user.is_bot,
        first_name=user.first_name,
    )
    return t_user
