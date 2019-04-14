from member.models import Bot
from member.runner import run_bot_with_handlers

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot = Bot.objects.first()
        run_bot_with_handlers(bot)
