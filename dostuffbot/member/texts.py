from core.utils import emojize


def command_menu(command):
    return (
        f'***Command***: {command.caller}\n'
        f'***Answer***: {command.get_answer_preview()}'
    )


def notification_sent(done_count, all_count):
    return emojize(f'Notification was sent to all subscribers. :white_check_mark:\n{done_count} / {all_count} :mega:')


def message_mailing_status(done_count, all_count):
    return emojize(f'Sending message to your subscribers.\n{done_count} / {all_count} :mega:')


def delete_command(command):
    return f'You are about to delete the command ***{command.caller}***. Is that correct?'
