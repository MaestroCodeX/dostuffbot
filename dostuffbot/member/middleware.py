import logging

from telegram.ext import ConversationHandler

from core.utils import get_fullname, get_telegram_user_from_update
from member.models import ErrorReport


def middleware(func):
    def func_wrapper(update, context):
        for middleware in MIDDLEWARES:
            middleware(update, context)

        try:
            next_state = func(update, context)
            context['state'] = next_state
            return next_state
        except Exception as e:
            logging.error(e)
            user_id = get_telegram_user_from_update(update).id
            ErrorReport.objects.create(
                user_id=user_id,
                context=context,
            )
            logging.info((
                f'Could not proceed the request for user {user_id or "unknown"}. '
                f'Exception of type {type(e)} was raised.'
            ))
            update.message.reply_text('Unexpected error. /start')
            return ConversationHandler.END
    return func_wrapper


def log_request(update, context):
    user = update.effective_user
    if not user:
        return

    user_sign = f'User {get_fullname(user)} {user.id}'
    if update.message:
        logging.info(f'{user_sign} sent message with text: {update.message.text}')
    elif update.callback_query:
        logging.info(f'{user_sign} sent callback with data: {update.callback_query.data}')


MIDDLEWARES = [
    log_request
]
