from . import views
from . import views_profile
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('register', views.UserRagistrationViewSet, basename='register')
router.register('verify', views.VerifyCodeViewSet, basename='verify_code')
router.register('resend-code', views.ResendCodeViewSet, basename='resend_code')
router.register('password-reset', views.PasswordResetViewSet, basename='reset-password')
router.register('confirm-password-reset', views.ConfirmResetPasswordViewSet, basename='confirm-reset-password')
router.register('profile', views_profile.ProfileViewSet, basename='profile')


app_name = 'auth'
urlpatterns = router.urls
