import logging

from core.utils import get_fullname


def middleware(func):
    def func_wrapper(bot, update):
        for middleware in MIDDLEWARES:
            middleware(bot, update)

        try:
            return func(bot, update)
        except Exception as e:
            logging.error(e)

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
