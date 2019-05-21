from core.utils import emojize, escape_markdown


def command_menu(command):
    return f'***Command***: {escape_markdown(command.caller)}\n\nSelect what you want to do:'


def notification_sent(done_count, all_count):
    return emojize(f'Notification was sent to all subscribers. :white_check_mark:\n{done_count} / {all_count} :mega:')


def message_mailing_status(done_count, all_count):
    return emojize(f'Sending message to your subscribers.\n{done_count} / {all_count} :mega:')


def delete_command(command):
    return f'You are about to delete the command ***{escape_markdown(command.caller)}***. Is that correct?'


def back_text(section):
    return f'« Back to {section}'


DELETE_COMMAND = 'Delete command'
SHOW_ANSWER = 'Show answer'
COMMANDS = 'Commands'
DELETE_COMMAND_CONFIRM = 'Yes, delete the command'
SEND_NOTIFICATION = 'Send notification'
SETTINGS = 'Settings'
ADD_COMMAND = 'Add command'
EDIT_COMMAND = 'Edit command'
EDIT_ANSWER = 'Edit answer'
SEND_NOTIFICATION = 'Send notification'
COMPLETE = 'Complete'
CANCEL = 'Cancel'
DELETE_ALL_MESSAGES = 'Delete all messages'
DELETE_LAST_MESSAGE = 'Delete last message'
SAVE_CHANGES = 'Save changes'
EXIT_NO_SAVE = 'Exit without any changes'
