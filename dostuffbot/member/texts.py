def command_menu(command):
    return (
        f'***Command***: {command.command}\n'
        f'***Answer***: {command.content}'
    )


def notification_sent(subs):
    return f'Notification was sent to all {subs.count()} active subscribers.'


def message_mailing_status(done_count, all_count):
    return (
        'Sending message to your subscribers.\n'
        f'{done_count} / {all_count}'
    )


COMMANDS = 'This is a list of your commands. Select command to see the details:'
NOTIFY_MESSAGE = 'Send a message that you want to share with your subscribers.'
NOTIFICATION_CANCELLED = 'Notification cancelled.'
START = 'Choose an option from the list below:'
