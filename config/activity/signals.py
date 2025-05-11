from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Activity


@receiver(user_logged_in)
def log_user_login(sender, user, request, **kwargs):
    Activity.objects.create(
        user=user,
        activity_type='login'
    )
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'activity_{user.id}',
        {
            'type': 'send_activity',
            'activity_type': 'login',
            'user': user.username,
        }
    )
