from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import ProfileUser
from .serializers import ProfileSerializers
from .permissions import OwnerOrReadOnly


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileSerializers
    

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [OwnerOrReadOnly()]
