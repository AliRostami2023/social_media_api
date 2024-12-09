from celery import shared_task
from .models import Notification
from django.contrib.auth import get_user_model
from post.models import Post


User = get_user_model()


@shared_task
def create_notifications_task(recipient_id, sender_id, notification_type, post_id=None, message=""):
    try:
        recipient = User.objects.get(id=recipient_id)
        sender = User.objects.get(id=sender_id)
        post = Post.objects.get(id=post_id) if post_id else None

        Notification.objects.create(
            recipient = recipient,
            sender = sender,
            notification_type = notification_type,
            post = post,
            message = message
        )
        return "Notification created successfully"

    except User.DoesNotExist:
        pass
    except Post.DoesNotExist:
        pass

