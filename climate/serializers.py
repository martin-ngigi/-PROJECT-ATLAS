from rest_framework import  serializers
from .models import Climate
from . import ClimateTypesEnum
from  django.core.validators import MinValueValidator, MaxValueValidator

class ClimateTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climate
        fields = "__all__"

class GeneralClimateSerializer(serializers.Serializer):
    climate_type = serializers.ChoiceField(
        choices=ClimateTypesEnum.ClimateTypes.choices(),
        help_text="i.e. Temperature, Precipitation"
    )
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    month = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12)
        ],
        required=False,  # use required instead of null=True/blank=True
        allow_null=True
    )
    start_date = serializers.DateField(
        input_formats=["%Y%m%d", "%Y-%m-%d"],
        format= ["%Y%m%d", "%Y-%m-%d"]
    )
    end_date = serializers.DateField(
        input_formats=["%Y%m%d", "%Y-%m-%d"],
        format= ["%Y%m%d", "%Y-%m-%d"]
    )

