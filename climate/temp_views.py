from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import temp_service
from .ncei.serializers import NCEIWeatherRequestSerializer
from .open_meteo.serializers import OpenMeteoWeatherRequestSerializer
from .nasa.serializers import NASAWeatherRequestSerializer
from .serializers import ClimateTemperatureSerializer, GeneralClimateSerializer
import logging

class AggregatedTemperatureView(APIView):
    def post(self, request):
        # Extract nested payloads
        general = request.data.get("general", {})
        open_meteo_data = request.data.get("open_meteo", {})
        ncei_data = request.data.get("ncei", {})
        nasa_data = request.data.get("nasa", {})

        # Validate each serializer with its nested data
        general_serializer = GeneralClimateSerializer(data=general)
        open_meteo_serializer = OpenMeteoWeatherRequestSerializer(data=open_meteo_data)
        # ncei_serializer = NCEIWeatherRequestSerializer(data=ncei_data)
        nasa_serializer = NASAWeatherRequestSerializer(data=nasa_data)

        # Validate each serializer explicitly
        general_valid = general_serializer.is_valid()
        open_meteo_valid = open_meteo_serializer.is_valid()
        # ncei_valid = ncei_serializer.is_valid()
        nasa_valid = nasa_serializer.is_valid()


        if not (open_meteo_valid and nasa_valid and general_valid):
            logging.error(
                f"❌ Errors: "
                f"general={general_serializer.errors}, "
                f"open_meteo={open_meteo_serializer.errors}, "
                # f"ncei={ncei_serializer.errors}, "
                f"nasa={nasa_serializer.errors}"
            )
            return Response(
                {
                    "general": general_serializer.errors,
                    "open_meteo_errors": open_meteo_serializer.errors,
                    # "ncei_errors": ncei_serializer.errors,
                    "nasa_errors": nasa_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            aggregated = temp_service.aggregare_monthly_avg_temperature(
                general_kwargs=general_serializer.validated_data,
                nasa_kwargs=nasa_serializer.validated_data,
                # ncei_kwargs=ncei_serializer.validated_data,
                open_meteo_kwargs=open_meteo_serializer.validated_data
            )

            # Serialize each years separately
            grouped = {}
            for year_str, records in aggregated.items():
                serializer = ClimateTemperatureSerializer(records, many=True)
                grouped[year_str] = serializer.data

            logging.info(f"✅ Temperature aggregated successfully.")
            return Response(grouped, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"❌ Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
