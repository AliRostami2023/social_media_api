from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CreateMixin(models.Model):
    created = models.DateTimeField(default=timezone.now, verbose_name=_('created'))

    class Meta:
        abstract = True
    

class UpdateMixin(models.Model):
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))

    class Meta:
        abstract = True
        