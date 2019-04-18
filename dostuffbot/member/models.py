from django.db import models

from core.models import CreatedUpdatedModel
from main.models import User
from member import constants


class BotAccessManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(bot__id=constants.BOT_ID)


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
    text = models.CharField(max_length=40)
    content = models.CharField(max_length=400)


class Subscriber(CreatedUpdatedModel):
    objects = BotAccessManager()

    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )
