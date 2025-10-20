from rest_framework import serializers
class OpenMeteoWeatherRequestSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    daily = serializers.CharField(required=False, default="temperature_2m_mean")

class GeneralOpenMeteoWeatherRequestSerializer(serializers.Serializer):
        daily = serializers.CharField(required=False, default="temperature_2m_mean")