from rest_framework import serializers
# https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN&community=AG&longitude=1.7471&latitude=40.0573&start=20240101&end=20241231&format=JSON
class NASAWeatherRequestSerializer(serializers.Serializer):
    parameters = serializers.CharField(required=False, default="T2M,T2M_MAX,T2M_MIN")
    community = serializers.CharField(required=False, default="AG") #AG (Agroclimatology - agricultural), RE (Renewable Energy - renewable energy), SB (Sustainable Infrastructure - Sustainable Buildings) 
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    format = serializers.CharField(required=False, default="JSON") 
    start = serializers.DateField(required=True, input_formats=["%Y%m%d"])
    end = serializers.DateField(required=True, input_formats=["%Y%m%d"])

    def validate(self, data):
        # Convert back to NASA expected format YYYYMMDD
        data["start"] = data["start"].strftime("%Y%m%d")
        data["end"] = data["end"].strftime("%Y%m%d")
        return data