from django.db import models

from core.enums import CommandMessageType, CommandStatus
from core.models import CreatedUpdatedModel, ManagerActive
from main.models import User


class CommandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=CommandStatus.DONE)


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


class Subscriber(CreatedUpdatedModel):
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )


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

    objects = CommandManager()
    all = models.Manager()

    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='commands',
    )
    status = models.CharField(max_length=20, choices=CommandStatus)
    caller = models.CharField(max_length=40)

    def reply_to(self, message):
        msg_qs = self.command_messages.all()
        for msg in msg_qs:
            context = msg.get_context()
            func_name = msg.get_func_name()
            getattr(message, func_name)(**context, parse_mode='MARKDOWN')


class CommandMessage(CreatedUpdatedModel):

    objects = ManagerActive()
    all = models.Manager()

    command = models.ForeignKey(
        Command,
        on_delete=models.CASCADE,
        related_name='command_messages',
    )
    type = models.CharField(max_length=20, choices=CommandMessageType)
    text = models.TextField(blank=True, null=True)
    file_id = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)

    def get_context(self):
        if self.type == CommandMessageType.TEXT:
            return {'text': self.text}

        media_field = self.type.lower()
        return {media_field: self.file_id, 'caption': self.text}

    def get_func_name(self):
        media_field = self.type.lower()
        return f'reply_{media_field}'


class ErrorReport(CreatedUpdatedModel):
    user_id = models.IntegerField(blank=True, null=True)
    error = models.TextField()
    context = models.TextField()
