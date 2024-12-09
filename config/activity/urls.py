from django.urls import path
from . import views


app_name = 'active'
urlpatterns = [
    path('', views.ActivityGenericView.as_view(), name='activity_view'),
]
