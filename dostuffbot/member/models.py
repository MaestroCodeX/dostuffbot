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
        related_name='subscriber_set',
    )


class BotAdmin(CreatedUpdatedModel):
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='admin_set',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_set',
    )
    is_owner = models.BooleanField(default=False)


class Command(CreatedUpdatedModel):
    """ The model is used to store command of the bot that it can answer. """

    objects = CommandManager()
    all = models.Manager()

    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='command_set',
    )
    status = models.CharField(max_length=20, choices=CommandStatus)
    caller = models.CharField(max_length=40)

    def reply_to(self, message):
        msg_qs = self.message_set.all()
        for msg in msg_qs:
            context = msg.get_context()
            func_name = msg.get_func_name()
            getattr(message, func_name)(**context, parse_mode='MARKDOWN')


class CommandMessage(CreatedUpdatedModel):
    """ The model is used to store a single message of the command answer.
    It can either be some text or a media like image, video or audio. """

    objects = ManagerActive()
    all = models.Manager()

    command = models.ForeignKey(
        Command,
        on_delete=models.CASCADE,
        related_name='message_set',
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
    """ Model to store unhandled errors that was raised when preceding the request.
    There is user id, actual error and context of the user at that moment.
    This is used to find problems. """

    user_id = models.IntegerField(blank=True, null=True)
    error = models.TextField()
    context = models.TextField()
