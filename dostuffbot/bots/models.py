from django.db import models

from accounts.models import User


class Bot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
