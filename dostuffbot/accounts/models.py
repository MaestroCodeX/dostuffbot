from django.db import models
from telegram import CallbackQuery, User as TelegramUser
from telegram.error import BadRequest


class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    lang = models.CharField(max_length=10, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    dialog_id = models.IntegerField(blank=True, null=True)

    def get_telegram_user(self):
        user = TelegramUser(id=self.id, is_bot=self.is_bot, first_name=self.first_name)
        return user

    def update_dialog(self, bot, new_dialog_id):
        """ Delete previous CallbackQuery dialog and save new one. """
        if self.dialog_id:
            try:
                bot.delete_message(chat_id=self.id, message_id=self.dialog_id)
            except BadRequest:
                pass

        self.dialog_id = new_dialog_id
        self.save()

    def get_dialog(self):
        t_user = self.get_telegram_user()
        query = CallbackQuery(id=self.dialog_id, from_user=t_user, chat_instance=self.dialog_id)
        print(query)
        return query
