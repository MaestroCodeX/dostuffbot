from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    lang = models.CharField(max_length=10, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    dialog_id = models.IntegerField(blank=True, null=True)

    def update_dialog(self, bot, message):
        """ Delete previous CallbackQuery dialog and save new one. """
        if self.dialog_id:
            bot.delete_message(chat_id=self.id, message_id=self.dialog_id)

        self.dialog_id = message.message_id
        self.save()
