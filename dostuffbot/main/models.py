from django.db import models
from telegram.error import BadRequest


class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    lang = models.CharField(max_length=10, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    dialog_id = models.IntegerField(blank=True, null=True)

    def update_dialog(self, bot, new_dialog_id):
        """ Delete previous CallbackQuery dialog and save new one. """
        if self.dialog_id:
            try:
                bot.delete_message(chat_id=self.id, message_id=self.dialog_id)
            except BadRequest:
                pass

        self.dialog_id = new_dialog_id
        self.save()


class Bot(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bot_set',
    )
    token = models.CharField(max_length=100)

    @property
    def full_username(self):
        return '@' + self.username
