from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from core.models import CreateMixin, UpdateMixin

User = get_user_model()


# class Hashtag(models.Model):
#     name = models.CharField(max_length=500, default="#", verbose_name=_('hashtag name'))

#     def __str__(self):
#         return self.name


class PostManager(models.Manager):
    def published(self):
        return self.filter(public=True)


class Post(CreateMixin, UpdateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    title = models.CharField(max_length=300, verbose_name=_('title'))
    slug = models.CharField(max_length=50, unique=True, verbose_name=_('slug'))
    description = models.TextField(max_length=2048, verbose_name=_('description'), null=True, blank=True)
    image = models.ImageField(upload_to='post_image/%y/%m/%d', verbose_name=_('image'), null=True)
    video = models.FileField(upload_to='video_post/%y/%m/%d', verbose_name=_('video'), null=True)
    public = models.BooleanField(default=True, verbose_name=_('public / private'))
    orginal_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='shared_post')
    is_repost = models.BooleanField(default=False)

    objects = PostManager()

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Post.objects.get(pk=self.pk).title != self.title):
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            num = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.title
    
    
    @property
    def likes_count(self):
        return self.post_like.count()
    

    class Meta:
        ordering = ['-created']



class LikePost(CreateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

    def __str__(self) -> str:
        return self.user.username



class Comment(CreateMixin, UpdateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cuser')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='cpost')
    body = models.TextField(max_length=1024, verbose_name=_('content'))
    parent = models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.body[:20]}"
    
    class Meta:
        ordering = ['-created']
