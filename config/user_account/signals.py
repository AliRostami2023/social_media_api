from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import ProfileUser


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_user(sender, **kwargs):
    if kwargs['created']:
        ProfileUser.objects.create(user=kwargs['instance'])
        