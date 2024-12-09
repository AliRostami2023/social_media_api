from django.utils import timezone
from django.urls import resolve
from .models import Activity
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from .tasks import log_activity_task

User = get_user_model()


class ProfileViewActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return

        current_url_name = resolve(request.path_info).url_name
        if current_url_name == 'profile':
            profile_user_id = view_kwargs.get('user_id')
            if profile_user_id and int(profile_user_id) != request.user.id:
                today = timezone.now().date()
                already_viewed = Activity.objects.filter(
                    user=request.user,
                    activity_type='view',
                    viewed_page=current_url_name,
                    timestamp__date=today
                ).exists()

                if not already_viewed:
                    log_activity_task.delay(
                        user=request.user.id,
                        activity_type='view',
                        viewed_page=current_url_name,
                    )
