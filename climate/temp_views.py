from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import utils.country_service
from utils.date_formater import convert_date_format
from . import temp_service
from .ncei.serializers import NCEIWeatherRequestSerializer
from .open_meteo.serializers import OpenMeteoWeatherRequestSerializer, GeneralOpenMeteoWeatherRequestSerializer
from .nasa.serializers import NASAWeatherRequestSerializer, GeneralNASAWeatherRequestSerializer
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
        open_meteo_serializer = GeneralOpenMeteoWeatherRequestSerializer(data=open_meteo_data)
        # ncei_serializer = NCEIWeatherRequestSerializer(data=ncei_data)
        nasa_serializer = GeneralNASAWeatherRequestSerializer(data=nasa_data)

        # Validate each serializer explicitly
        general_valid = general_serializer.is_valid()
        open_meteo_valid = open_meteo_serializer.is_valid()
        # ncei_valid = ncei_serializer.is_valid()
        nasa_valid = nasa_serializer.is_valid()

        if not (open_meteo_valid and nasa_valid and general_valid):
            logging.error(
                f"❌ Errors AggregatedTemperatureView: "
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
            general_kwargs = general_serializer.validated_data
            open_meteo_validated_data = open_meteo_serializer.validated_data
            nasa_validated_data = nasa_serializer.validated_data

            # Define all default general kwargs in a single map
            open_meteo_general_values = {
                "longitude": general_kwargs["longitude"],
                "latitude": general_kwargs["longitude"],
                "start_date": general_kwargs["start_date"],
                "end_date": general_kwargs["end_date"],
            }

            nasa_general_values = {
                "longitude": general_kwargs["longitude"],
                "latitude": general_kwargs["longitude"],
                "start": convert_date_format(str(general_kwargs["start_date"])),  #.replace("-", ""),
                "end": convert_date_format(str(general_kwargs["end_date"])) #.replace("-", ""),
            }

            # Merge defaults with validated data — validated data takes priority
            open_meteo_kwargs = {**open_meteo_general_values, **open_meteo_validated_data}
            nasa_kwargs = {**nasa_general_values, **nasa_validated_data}


            country_details = utils.country_service.get_country_details(general_kwargs["latitude"], general_kwargs["longitude"])
            country_code = country_details["countryCode"]
            country_name = country_details["countryName"]

            general_kwargs.setdefault("measurement_unit", "T2M")
            general_kwargs.setdefault("unit_standardized", "Celsius")
            general_kwargs.setdefault("source", "aggregated")
            general_kwargs.setdefault("aggregation_method", "mean")
            general_kwargs.setdefault("country_name", country_name)
            general_kwargs.setdefault("country_code", country_code)

            aggregated = temp_service.aggregare_monthly_avg_temperature(
                general_kwargs=general_kwargs,
                nasa_kwargs=nasa_kwargs,
                # ncei_kwargs=ncei_serializer.validated_data,
                open_meteo_kwargs=open_meteo_kwargs
            )

            logging.info(f"AggregatedTemperatureView: aggregated count ={len(aggregated)}")
            serializer = ClimateTemperatureSerializer(aggregated, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(f"❌ Error AggregatedTemperatureView: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
