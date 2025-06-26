from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'image', 'video', 'public', 'orginal_post', 'is_repost']
    list_filter = ['is_repost', 'public']
    list_per_page = 50
    search_fields = ['user', 'title']
    raw_id_fields = ['user']


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created']
    raw_id_fields = ['user', 'post']
    list_per_page = 100
    search_fields = ['user', 'post']


@admin.register(Comment)
class CommentPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'body', 'parent', 'created']
    list_per_page = 50
    raw_id_fields = ['user', 'post', 'parent']
    search_fields = ['user', 'post']