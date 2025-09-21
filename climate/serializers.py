from rest_framework import  serializers
from .models import ClimateTemperature

class ClimateTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateTemperature
        fields = "__all__"