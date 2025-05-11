from django.urls import path, re_path
from . import views


app_name = 'home'

urlpatterns = [
    path('posts/', views.ListPostAPIView.as_view(), name='post-list'),
    path('posts/create/', views.CreatePostAPIView.as_view(), name='create_post'),
    re_path(r'posts/detail/(?P<slug>[-\wآ-ی]+)/', views.DetailPostAPIView.as_view(), name='detail_post'),
    path('posts/update/<int:pk>/', views.UpdatePostAPIView.as_view(), name='update_post'),
    path('posts/delete/<int:pk>/', views.DeletePostAPIView.as_view(), name='delete_post'),
    path('posts/<int:post_id>/update-comment/<int:pk>/', CommentDetailUpdateApiView.as_view()),
    path('posts/<int:post_id>/comments/', CommentCreateListApiView.as_view()),
    path('posts/<int:post_id>/update-comment/<int:pk>/', CommentDetailUpdateApiView.as_view()),
]
