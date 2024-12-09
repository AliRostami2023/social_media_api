from celery import shared_task
from .models import Activity
from post.models import Post, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model
import logging


logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task
def log_activity_task(user_id, activity_type, post_id=None, comment_id=None, viewed_page=None):
    logger.info(f"Logging activity for user {user_id} with activity type {activity_type}")
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

    logger.info("Activity logged successfully.")
    