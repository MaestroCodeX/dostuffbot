from telegram.ext import Dispatcher
from django.db import models

from core.enums import CommandMessageType
from core.models import CreatedUpdatedModel
from main.models import User


class BotAccessManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        bot = Dispatcher.get_instance().db_bot
        return queryset.filter(bot=bot)


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
    objects = BotAccessManager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bot_admins',
    )
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='admins',
    )
    is_owner = models.BooleanField(default=False)


class Command(CreatedUpdatedModel):
    objects = BotAccessManager()

    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='commands',
    )
    caller = models.CharField(max_length=40)

    def save(self, *args, **kwargs):
        if not self.pk:
            db_bot = Dispatcher.get_instance().db_bot
            self.bot = db_bot

        super().save(*args, **kwargs)

    def get_answer_preview(self):
        messages = self.command_messages.all()
        answer = ''
        if messages.exclude(type=CommandMessageType.TEXT).exists():
            for key, value in CommandMessageType:
                msgs_count = messages.filter(type=value).count()
                if msgs_count:
                    answer += f'[{msgs_count} {key.lower()} message{"s" if msgs_count > 1 else ""}]\n'
        else:
            text_message = messages.first()
            if not text_message:
                return r'\[No content]'
            else:
                answer += text_message.text[:50]
                if text_message.text_length > 50:
                    answer += '...'
                msgs_count = messages.count()
                if msgs_count > 1:
                    answer += f'\n[and {msgs_count - 1} text message{"s" if msgs_count > 2 else ""} more...]'
        return answer


class CommandMessage(CreatedUpdatedModel):
    command = models.ForeignKey(
        Command,
        on_delete=models.CASCADE,
        related_name='command_messages',
    )
    type = models.CharField(max_length=20, choices=CommandMessageType)
    text = models.TextField(blank=True, null=True)
    text_length = models.IntegerField(default=0)
    files = models.CharField(max_length=40, blank=True, null=True)
    images = models.CharField(max_length=40, blank=True, null=True)
    videos = models.CharField(max_length=40, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.text_length = len(self.text)
        super().save(*args, **kwargs)


class Subscriber(CreatedUpdatedModel):
    objects = BotAccessManager()

    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )
