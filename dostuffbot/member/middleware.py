import logging
import inspect

from core.utils import get_fullname, get_telegram_user_from_update


def middleware(func):
    def func_wrapper(*args, **kwargs):
        for middleware in MIDDLEWARES:
            middleware(*args, **kwargs)

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            kwargs = inspect.getcallargs(func, *args, **kwargs)
            update = kwargs.get('update')
            bot = kwargs.get('bot')
            if not all((update, bot)):
                logging.info(f'Exception of type {type(e)} was raised.')
                return
            user_id = get_telegram_user_from_update(update).id or 'unknown'
            logging.info(f'Could not proceed the request for user {user_id}. Exception of type {type(e)} was raised.')

    return func_wrapper


def log_request(bot, update):
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
