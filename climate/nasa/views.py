from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import services
from .serializers import NASAWeatherRequestSerializer
import logging

"""
APIView for fetching daily weather data from Open-Meteo API.
sample url = https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN&community=AG&longitude=1.7471&latitude=40.0573&start=20240101&end=20241231&format=JSON
"""
class NASADailyTemperatureView(APIView):
    def post(self, request):
        serializer = NASAWeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logging.error(f"❌ Error NASADailyTemperatureView: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = services.get_monthly_temperature(**serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class NASAMonthlyTemperatureView(APIView):
    def post(self, request):
        serializer = NASAWeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logging.error(f"❌ Error NASAMonthlyTemperatureView: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = services.get_monthly_avg_temperature(**serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)