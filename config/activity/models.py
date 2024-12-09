from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreateMixin
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Activity(CreateMixin):
    ACTIVITY_TYPE = (
        ('like', 'like'),
        ('comment', 'comment'),
        ('login', 'login'),
        ('view', 'view'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_activity', verbose_name=_('user'))
    activity_type = models.CharField(_('activity type'), max_length=20, choices=ACTIVITY_TYPE)
    post = models.ForeignKey('post.Post', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='post_activity', verbose_name=_('post'))
    comment = models.ForeignKey('post.Comment', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='comment_activity', verbose_name=_('comment'))
    viewed_page = models.URLField(_('viewed page'), null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.user.username} - {self.activity_type}"
