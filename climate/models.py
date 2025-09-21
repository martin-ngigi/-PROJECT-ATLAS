from django.db import models
import uuid
from  django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class ClimateTemperature(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    longitude = models.FloatField()
    latitude =  models.FloatField()
    month =  models.IntegerField(
        validators=[
            MinValueValidator(12),
            MaxValueValidator(0)
        ],
        null=True,
        blank=True
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField()

    open_meteo_value = models.FloatField(blank=True, null=True)
    nasa_value = models.FloatField(blank=True, null=True)
    ncei_value = models.FloatField(blank=True, null=True)

    mean_value = models.FloatField(blank=True, null=True)
    value = models.FloatField(
        blank=True,
        null=True,
        help_text="Store same as mean_value (but allows flexibility if different calc later)"
    )
    measurement_unit = models.CharField(max_length=20)
    unit_standardized = models.CharField(max_length=20, default="Celsius")

    source = models.CharField(max_length=50, default="aggregated")
    aggregation_method = models.CharField(max_length=50, default="mean")

    country = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text= "Set once"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        help_text= "Updated on Save"
    )

    class Meta:
        db_table = "climate_temperature"
        indexes = [
            models.Index(fields=["latitude", "longitude", "year" ])
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return  f"{self.year} | {self.latitude}, {self.longitude} -> {self.mean_value}"
