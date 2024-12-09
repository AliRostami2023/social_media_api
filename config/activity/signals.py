from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
from post.models import LikePost, Comment
from .tasks import log_activity_task



@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    log_activity_task.delay(user.id, activity_type='login')


@receiver(post_save, sender=LikePost)
def create_like_activity(sender, instance, created, **kwargs):
    if created:
        log_activity_task.delay(
            instance.user.id,
            'like',
            post_id=instance.post.id,
        )


@receiver(post_save, sender=Comment)
def create_comment_activity(sender, instance, created, **kwargs):
    if created:
        log_activity_task.delay(
            instance.user.id,
            'comment',
            post_id=instance.post.id,
            comment_id=instance.id,
        )
