from django.db import models

from core.models import CreatedUpdatedModel


class User(CreatedUpdatedModel):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    lang = models.CharField(max_length=10, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    dialog_id = models.IntegerField(blank=True, null=True)

    def update_dialog(self, bot, func, context):
        """ Delete previous CallbackQuery dialog and send new one. """
        if self.dialog_id:
            try:
                bot.delete_message(chat_id=self.id, message_id=self.dialog_id)
            except Exception:
                bot.edit_message_text(chat_id=self.id, message_id=self.dialog_id, text='-')

        sent_message = func(**context)
        self.dialog_id = sent_message.message_id
        self.save()


class Faq(CreatedUpdatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='faq_set',
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()


class FaqRate(CreatedUpdatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='faq_rates',
    )
    faq = models.ForeignKey(
        Faq,
        on_delete=models.CASCADE,
        related_name='rates',
    )
    is_positive = models.BooleanField(default=True)
