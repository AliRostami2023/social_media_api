from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializers
from rest_framework import permissions


class ActivityGenericView(generics.ListAPIView):
    serializer_class = ActivitySerializers
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by('-created')
