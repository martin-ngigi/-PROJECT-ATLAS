from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import services
from .serializers import OpenMeteoWeatherRequestSerializer
import logging

"""
APIView for fetching daily weather data from Open-Meteo API.
sample url = "https://archive-api.open-meteo.com/v1/archive?latitude=1.75&longitude=40.05&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean&timezone=auto"
"""
class DailyWeatherView(APIView):
    def post(self, request):
        serializer = OpenMeteoWeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logging.error(f"❌ Error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = services.get_daily_weather(**serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MonthlyWeatherView(APIView):
    def post(self, request):
        serializer = OpenMeteoWeatherRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logging.error(f"❌ Error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = services.get_monthly_avg_temperature(**serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)