from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/group/(?P<group_id>\d+)/$', consumers.ActivityConsumer.as_asgi()),
]
