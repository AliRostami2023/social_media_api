from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .serializers import FollowerSerializers, NotificationsSerializers
from .models import Follower, Notification
from .tasks import create_notifications_task


User = get_user_model()


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.select_related('follower', 'followed')
    serializer_class = FollowerSerializers
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            if 'followers' in self.request.query_params:
                return Follower.objects.select_related('follower', 'followed').filter(followed=user)
            elif 'following' in self.request.query_params:
                return Follower.objects.select_related('follower', 'followed').filter(follower=user)
        return super().get_queryset()
    

    def create(self, request, *args, **kwargs):
        follower = request.user
        followed_id = request.data.get('followed')

        if not followed_id:
            return Response({'error': _('The followed user ID is required.')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            followed_id = int(followed_id)
        except ValueError:
            return Response({'error': _('Invalid followed user ID.')}, status=status.HTTP_400_BAD_REQUEST)

        if follower.id == followed_id:
            return Response({'error': _('you cant follow yourself')}, status.HTTP_400_BAD_REQUEST)
        
        if Follower.objects.filter(follower=follower, followed_id=followed_id).exists():
            return Response({'error': _('you are already following this user')}, status.HTTP_400_BAD_REQUEST)
        
        Follower.objects.create(follower=follower, followed_id=followed_id)

        follower_user = User.objects.get(id=followed_id)
        if follower_user != request.user:
            NotificationsViewSet.perform_create(
                serializer=NotificationsSerializers(data={
                    'recipient': follower_user.id,
                    'sender': follower.id,
                    'notification_type': 'follow',
                })
            )
            return Response({'status': 'followed'}, status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        follower = request.user
        followed_id = self.kwargs.get('pk')

        try:
            instance = Follower.objects.get(follower=follower, followed_id=followed_id)
            instance.delete()
            return Response({'status': _('unfollowed')}, status.HTTP_200_OK)
        except Follower.DoesNotExist:
            return Response({'error': _('you are not following this user')}, status.HTTP_400_BAD_REQUEST)
        

    def get_permissions(self, *args, **kwargs):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return super().get_permissions(*args, **kwargs)



class NotificationsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.select_related('recipient', 'sender', 'post')
    serializer_class = NotificationsSerializers
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user).order_by('-timestamp')
    

    def perform_create(self, serializer):
        instance = serializer.save()
        sender_id = self.request.user.id

        if instance.notification_type == 'follow':
            recipient_id = instance.recipient.id
            message = _(f"{self.request.user.username} started following you !")
        
        elif instance.notification_type == 'comment':
            if not instance.post:
                raise ValidationError(_("Post is required for a 'comment' notification."))
            recipient_id = instance.post.user.id
            message = _(f"{self.request.user.username} commented on your post !")

        elif instance.notification_type == 'like':
            if not instance.post:
                raise ValidationError(_("Post is required for a 'like' notification."))
            recipient_id = instance.post.user.id
            message = _(f"{self.request.user.username} liked your post.")
        
        elif instance.notification_type == 'share':
            if not instance.post:
                raise ValidationError(_('Post is required for a "share" notification.'))
            recipient_id = instance.post.user.id
            message = _(f"{self.request.user.username} shared your post.")

        else:
            raise ValidationError(_("Invalid notification type."))
        

        create_notifications_task.delay(
            recipient_id = recipient_id,
            sender_id = sender_id,
            notification_type = instance.notification_type,
            post = instance.post.id if instance.post else None,
            message = message
        )
