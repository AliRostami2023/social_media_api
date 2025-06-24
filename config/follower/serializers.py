from rest_framework import serializers
from .models import Follower



class FollowerSerializers(serializers.ModelSerializer):
    follower = serializers.CharField(read_only=True, source="follower.username")
    followed = serializers.CharField(read_only=True, source="followed.username")

    class Meta:
        model = Follower
        fields = ['id', 'follower', 'followed']

        