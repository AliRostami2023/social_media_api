from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .serializers import FollowerSerializers
from .models import Follower
from .utils import create_and_send_notification


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
            create_and_send_notification(
                recipient_id=follower_user.author.id, 
                sender_id=follower_user.id,    
                notification_type='follow',
                message= _(f"{follower_user.author.username} start folloeed you !")
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

