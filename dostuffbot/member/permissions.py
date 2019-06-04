from member.models import BotAdmin


def admin_only(func):
    """ Wrapper function to validate if the user is admin.
    If user is not an admin then do nothing. """

    def func_wrapper(update, context):
        user_id = update.effective_user.id
        if not BotAdmin.objects.filter(bot=context.bot.db_bot, user__id=user_id).exists():
            return
        return func(update, context)
    return func_wrapper


def subscriber_only(func):
    """ Wrapper function to validate if the user is not an admin.
    If user is an admin then do nothing. """

    def func_wrapper(update, context):
        user_id = update.effective_user.id
        if BotAdmin.objects.filter(bot=context.bot.db_bot, user__id=user_id).exists():
            return
        return func(update, context)
    return func_wrapper
