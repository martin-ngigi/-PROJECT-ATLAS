from rest_framework import serializers
class NCEIWeatherRequestSerializer(serializers.Serializer):
    datasetid = serializers.CharField(required=False, default="GHCND")
    datatypeid1 = serializers.CharField(required=False, default="TMIN")
    datatypeid2 = serializers.CharField(required=False, default="TMAX")
    startdate = serializers.DateField(required=True) # Format: YYYY-MM-DD i.e. 2024-01-01
    enddate = serializers.DateField(required=True)   # Format: YYYY-MM-DD i.e. 2024-12-31
    limit = serializers.IntegerField(required=False, default=1000)
    bbox = serializers.CharField(
        required=True,
        help_text="Bounding box coordinates in the format 'min_lon,min_lat,max_lon,max_lat'. Example: '34.0,-10.0,36.0,-8.0' for a box covering a specific area.",
        )