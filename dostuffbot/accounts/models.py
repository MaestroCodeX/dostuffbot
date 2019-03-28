from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    language_code = models.CharField(max_length=10)
    is_bot = models.BooleanField(default=False)


class Bot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
