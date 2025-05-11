from rest_framework import serializers
from .models import Activity



class ActivitySerializers(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Activity
        fields = '__all__'
        