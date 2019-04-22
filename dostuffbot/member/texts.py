from django.utils.translation import gettext as _


def command_menu(command):
    command_text = _('command')
    answer_text = _('answer')
    return (
        f"***{command_text}***: {command.command}\n"
        f"***{answer_text}***: {command.content}"
    )
