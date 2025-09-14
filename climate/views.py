from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .services import get_weather
from . import services
# Create your views here.

class DailyWeatherView(APIView):
    def get(self, request):
        lat = request.query_params.get("lat", "1.2921") # Default to Nairobi
        lon = request.query_params.get("lon", "36.8219") # Default to Nairobi
        try:
            data = services.get_daily_weather(
                latitude=lat,
                longitude=lon,
                start_date="2024-01-01",
                end_date="2024-12-31",
                daily="temperature_2m_mean"
                )
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MonthlyWeatherView(APIView):
    def get(self, request):
        lat = request.query_params.get("lat", "1.2921") # Default to Nairobi
        lon = request.query_params.get("lon", "36.8219") # Default to Nairobi
        try:
            data = services.get_monthly_avg_temperature(
                latitude=lat,
                longitude=lon,
                start_date="2024-01-01",
                end_date="2024-12-31",
                daily="temperature_2m_mean"
                )
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
