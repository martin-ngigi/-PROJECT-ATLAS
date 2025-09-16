from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import services
from .serializers import WeatherRequestSerializer
import logging

"""
Sample URL: https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&startdate=2024-01-01&enddate=2024-12-31&limit=1000&bbox=1.8,40.0,1.7,40.1
Don't forget to add token: "" as a header.
"""

class NCEIDailyWeatherView(APIView):
    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logging.error(f"❌ Error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = services.get_daily_weather(**serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class NCEIMonthlyWeatherView(APIView):
    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logging.error(f"❌ Error:s {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = services.get_monthly_avg_temperature(**serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)