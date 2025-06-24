from django.urls import path, re_path
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.ListPostAPIView.as_view(), name='post-list'),
    path('posts/create/', views.CreatePostAPIView.as_view(), name='create_post'),
    re_path(r'posts/detail/(?P<slug>[-\wآ-ی]+)/', views.DetailPostAPIView.as_view(), name='detail_post'),
    path('posts/update/<int:pk>/', views.UpdatePostAPIView.as_view(), name='update_post'),
    path('posts/delete/<int:pk>/', views.DeletePostAPIView.as_view(), name='delete_post'),
    re_path(r'^(?P<post_slug>[-\wآ-ی]+)/comments/', views.ListCommentAPIView.as_view(), name='comment-list'),
    re_path(r'^(?P<post_slug>[-\wآ-ی]+)/create_comment/', views.CommentCreateListApiView.as_view(), name='comment-create'),
    re_path(r'^(?P<post_slug>[-\wآ-ی]+)/(?P<comment_id>\d+)/reply/', views.ReplyCreateAPIView.as_view(), name='comment-reply'),
    re_path(r'^(?P<post_slug>[-\wآ-ی]+)/(?P<pk>\d+)/edit/', views.CommentUpdateApiView.as_view(), name='comment-edit'),
    re_path(r'^(?P<post_slug>[-\wآ-ی]+)/replies/(?P<pk>\d+)/edit/', views.ReplyUpdateDeleteAPIView.as_view(), name='reply-edit'),
]
