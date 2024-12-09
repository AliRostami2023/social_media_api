from rest_framework import serializers
from .models import Activity



class ActivitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        