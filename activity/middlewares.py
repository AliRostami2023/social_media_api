from django.urls import resolve
from datetime import timedelta
from django.utils import timezone
from .models import Activity
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User


class ProfileViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            resolved_url = resolve(request.path_info)
        if resolved_url.url_name == 'profile-detail':
            viewed_pk = view_kwargs.get('pk')
            if viewed_pk and viewed_pk != request.user.username:
                User.objects.get(id=viewed_pk)
                viewed_page = f"/profile/{viewed_pk}/"
                    
                recent_activity = Activity.objects.filter(
                    user=request.user,
                    activity_type='view',
                    viewed_page=viewed_page,
                    created_at__gte=timezone.now() - timedelta(hours=1)
                ).exists()
                
                if not recent_activity:
                    Activity.objects.create(
                        user=request.user,
                        activity_type='view',
                        viewed_page=viewed_page
                    )

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f'activity_{request.user.id}',
                        {
                            'type': 'send_activity',
                            'activity_type': 'view',
                            'user': request.user.username,
                            'viewed_page': f"/profile/{viewed_pk}/",
                        }
                    )
        return None
    