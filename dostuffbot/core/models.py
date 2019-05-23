from django.db import models
from django.utils import timezone


class ManagerActive(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
