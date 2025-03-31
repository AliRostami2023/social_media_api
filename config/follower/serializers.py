from rest_framework import serializers
from .models import Follower



class FollowerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['id', 'follower', 'followed']

        