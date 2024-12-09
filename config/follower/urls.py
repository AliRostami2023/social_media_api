from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('follow', views.FollowerViewSet, basename='follow')
router.register('notification', views.NotificationsViewSet, basename='notification')


app_name = 'follow'
urlpatterns = router.urls
