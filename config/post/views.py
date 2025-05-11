from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from uuid import uuid4
from .paginations import PostPaginations, CommentPaginations
from .serializers import *
from .models import *
from .permissions import IsAuthorOrReadOnly
from activity.utils import log_activity
from follower.utils import create_and_send_notification



class CreatePostAPIView(generics.CreateAPIView):
    queryset = Post.objects.select_related('user', 'orginal_post')
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]



class ListPostAPIView(generics.ListAPIView):
    pagination_class = PostPaginations
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.select_related('user', 'orginal_post').filter(
                Q(user=self.request.user) | Q(public=True))
        return Post.objects.select_related('orginal_post', 'user')



class DetailPostAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.select_related('user', 'orginal_post')
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'


class UpdatePostAPIView(generics.UpdateAPIView):
    queryset = Post.objects.select_related('user', 'orginal_post')
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeletePostAPIView(generics.DestroyAPIView):
    queryset = Post.objects.select_related('user', 'orginal_post')
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    


class ExplorePostAPIView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Post.objects.select_related('user', 'orginal_post').order_by('?')
    serializer_class = ExplorPostSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username']

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    

class CommentCreateListApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializers
    queryset = Comment.objects.select_related('parent', 'user', 'post')
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommentPaginations


    def perform_create(self, serializer):
        try:
            comment = serializer.save(user=self.request.user)

            post_author = comment.post.user
            if post_author != self.request.user:
                create_and_send_notification(
                    recipient_id= post_author.id,
                    sender_id= self.request.user.id,
                    post_id= comment.post.id,
                    notification_type= 'comment',
                    message= _(f"{post_author.username} commented in {comment.post}")
                )

                log_activity(
                    user_id=self.request.user.id,
                    activity_type='comment',
                    post_id=comment.post.id,
                )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in CommentCreateListApiView: {str(e)}")



class CommentDetailUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentUpdateSerializers
    queryset = Comment.objects.select_related('parent', 'user', 'post')
    permission_classes = [permissions.IsAuthenticated]
    

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthorOrReadOnly()]
        return super().get_permissions()


class LikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LikePost.objects.select_related('user', 'post')
    serializer_class = LikePostSerializers


    def create(self, request, post_pk=None):
        post = Post.objects.get(id=post_pk)
        user = request.user
        if LikePost.objects.filter(user=user, post=post).exists():
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        
        LikePost.objects.create(user=user, post=post)

        post_author = post.user
        if post_author != user:
                create_and_send_notification(
                    recipient_id= post_author.id,
                    sender_id= user.id,
                    post_id= post.id,
                    notification_type= 'like',
                    message= _(f"{post_author.username} liked you on {post}")
                    )
                
                log_activity(
                    user_id=user.id,
                    activity_type='like',
                    post_id=post.id,
                )
                
                return Response({'detail': 'Liked'}, status=status.HTTP_201_CREATED)


    def destroy(self, request, post_pk=None):
        post = Post.objects.get(id=post_pk)
        user = request.user
        like = LikePost.objects.filter(user=user, post=post).first()
        if not like:
            return Response({'detail': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)
        
        like.delete()
        return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        


class RepostViewSet(viewsets.ModelViewSet):
    serializer_class = RepostSerializers
    queryset = Post.objects.select_related('user', 'orginal_post')
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, post_pk=None):
        sender_id = request.user.id

        try:
            original_post = Post.objects.get(pk=post_pk)
            new_slug = slugify(f"{original_post.slug}-{uuid4()}")
            
            Post.objects.create(
                user=request.user,
                title=original_post.title,
                slug=new_slug,
                description=original_post.description,
                image=original_post.image,
                video=original_post.video,
                orginal_post=original_post,
                is_repost=True
            )

            create_and_send_notification(
                recipinet_id = original_post.user.id,
                sender_id = sender_id,
                notification_type = 'share',
                post_id= original_post.id,
                message= _(f"{request.user.username} reposted your post.")
            )

            return Response({'detail': 'Post reposted successfully.'}, status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
