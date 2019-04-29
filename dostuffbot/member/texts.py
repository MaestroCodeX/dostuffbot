def command_menu(command):
    return (
        f'***Command***: {command.command}\n'
        f'***Answer***: {command.get_answer_preview()}'
    )


def notification_sent(subs):
    return f'Notification was sent to all {subs.count()} active subscribers.'


def message_mailing_status(done_count, all_count):
    return (
        'Sending message to your subscribers.\n'
        f'{done_count} / {all_count}'
    )


def delete_command(command):
    return f'You are about to delete your command ***{command.caller}***. Is that correct?'
