def command_menu(command):
    return (
        f'***Command***: {command.command}\n'
        f'***Answer***: {command.content}'
    )


def notification_sent(subs):
    return f'Notification was sent to all {subs.count()} active subscribers.'


COMMANDS = 'This is a list of your commands. Select command to see the details:'
NOTIFY_MESSAGE = 'Send a message that you want to share with your subscribers.'
START = 'Choose an option from the list below:'
