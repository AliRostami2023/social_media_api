from .models import Activity
from post.models import Post, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging


logger = logging.getLogger(__name__)

User = get_user_model()


def log_activity(user_id, activity_type, post_id=None, comment_id=None, viewed_page=None):
    """
    ثبت فعالیت کاربر و ارسال آن به WebSocket
    """
    
    logger.info(f"Logging activity for user {user_id} with activity type {activity_type}")
    
    try:
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id) if post_id else None
        comment = Comment.objects.get(id=comment_id) if comment_id else None

        Activity.objects.create(
            user=user,
            post=post,
            comment=comment,
            activity_type=activity_type,
            created=timezone.now(),
            viewed_page=viewed_page,
        )

        activity_data = {
            'type': 'send_activity',
            'activity_type': activity_type,
            'user': user.username,
            'post_id': post_id,
            'comment_id': comment_id,
            'viewed_page': viewed_page,
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'activity_{user_id}',
            activity_data
        )

        logger.info("Activity logged and sent to WebSocket successfully.")
    
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except Post.DoesNotExist:
        logger.error(f"Post with id {post_id} does not exist.")
    except Comment.DoesNotExist:
        logger.error(f"Comment with id {comment_id} does not exist.")
    except Exception as e:
        logger.error(f"Error logging activity: {str(e)}")
