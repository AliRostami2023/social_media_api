from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from post.models import Post

User = get_user_model()


class Follower(models.Model):
    follower = models.ForeignKey(User, verbose_name=_('follower'), related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, verbose_name=_('following'), related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')
        


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', _('Like')),
        ('comment', _('Comment')),
        ('follow', _('Follow')),
        ('share', _('share')),
    )
    
    recipient = models.ForeignKey(User, verbose_name=_('recipient'), related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, verbose_name=_('sender'), related_name='sent_notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(_('notification type'), max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, verbose_name=_('post'), on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(_('message'), blank=True)
    read = models.BooleanField(_('read?'), default=False)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)


    def __str__(self):
        return f'{self.sender} {self.get_notification_type_display()} {self.recipient}'
