from django.db import models

from core.enums import CommandMessageType, CommandStatus
from core.models import CreatedUpdatedModel
from main.models import User


class Bot(CreatedUpdatedModel):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bot_set',
    )
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    token = models.CharField(max_length=100)

    @property
    def full_username(self):
        return '@' + self.username


class BotAdmin(CreatedUpdatedModel):
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='admins',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bot_admins',
    )
    is_owner = models.BooleanField(default=False)


class Command(CreatedUpdatedModel):
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='commands',
    )
    status = models.CharField(max_length=20, choices=CommandStatus)
    caller = models.CharField(max_length=40)
    amswer_preview = models.CharField(max_length=80)

    def reply_to(self, message):
        msg_qs = self.command_messages.all()
        for msg in msg_qs:
            context = msg.get_context()
            func_name = msg.get_func_name()
            getattr(message, func_name)(**context, parse_mode='MARKDOWN')

    def update_answer_preview(self):
        command_messages = self.command_messages.all()
        max_text_length = 500
        text_length = 0
        answer_preview = []
        text_count = 0
        for message in command_messages:
            if message.type == CommandMessageType.TEXT:
                chars_left = max_text_length - text_length
                if chars_left <= 0:
                    text_count += 1
                    continue
                block = {
                    'type': CommandMessageType.TEXT,
                    'show': 'full',
                    'limit': None
                }
                if len(message.text) > chars_left:
                    block['show'] = 'part'
                    block['limit'] = chars_left
                text_length += len(message.text)
                answer_preview.append(block)
        if text_count:
            block = {
                'type': CommandMessageType.TEXT,
                'show': 'count',
                'count': text_count,
            }
            answer_preview.append(block)
        self.answer_preview = answer_preview
        self.save(update_fields=answer_preview)

    def get_answer_preview(self):
        return 'answer'


class CommandMessage(CreatedUpdatedModel):
    command = models.ForeignKey(
        Command,
        on_delete=models.CASCADE,
        related_name='command_messages',
    )
    type = models.CharField(max_length=20, choices=CommandMessageType)
    text = models.TextField(blank=True, null=True)
    file_id = models.CharField(max_length=40)

    def get_context(self):
        if self.type == CommandMessageType.TEXT:
            return {'text': self.text}

        media_field = self.type.lower()
        return {media_field: self.file_id, 'caption': self.text}

    def get_func_name(self):
        media_field = self.type.lower()
        return f'reply_{media_field}'


class Subscriber(CreatedUpdatedModel):
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )
