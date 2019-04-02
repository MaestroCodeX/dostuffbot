from django.db import models

from accounts.models import User


class Bot(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bot_set',
    )
    token = models.CharField(max_length=100)
