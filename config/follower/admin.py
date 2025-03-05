from django.contrib import admin
from .models import Notification, Follower



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'post', 'message', 'read', 'timestamp',]
    list_filter = ['notification_type', 'read']
    list_per_page = 100
    raw_id_fields = ['recipient', 'sender']


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['follower', 'followed']
    raw_id_fields = ['follower', 'followed']
    list_per_page = 100
