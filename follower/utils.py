from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def create_and_send_notification(recipient_id, sender_id, notification_type, post_id=None, message=""):
    notification = Notification.objects.create(
        recipient_id=recipient_id,
        sender_id=sender_id,
        notification_type=notification_type,
        post_id=post_id,
        message=message,
        read=False,
        timestamp=timezone.now()
    )

    channel_layer = get_channel_layer()
    group_name = f'user_{recipient_id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'sender': str(notification.sender.username),
            'notification_type': notification.get_notification_type_display(),
            'message': notification.message,
            'post_id': notification.post_id if notification.post else None,
            'timestamp': notification.timestamp.isoformat(),
            'read': notification.read
        }
    )
    
    return notification
