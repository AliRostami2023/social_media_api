from django.db import models
from django.utils import timezone


class CreateMixin(models.Model):
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
    

class UpdateMixin(models.Model):
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        