from django.urls import path
from .views import *
from rest_framework import routers
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('explore', ExplorePostViewSet, basename='explore')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('repost', RepostViewSet, basename='repost')
post_router.register('likes', LikeViewSet, basename='like')


app_name = 'home'
urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentCreateListApiView.as_view()),
    path('posts/<int:post_id>/update-comment/<int:pk>/', CommentDetailUpdateApiView.as_view()),
]

urlpatterns += router.urls + post_router.urls

