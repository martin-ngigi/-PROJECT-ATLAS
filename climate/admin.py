from django.contrib import admin

# Register your models here.
from .models import Climate

# admin.site.register(ClimateTemperature)
@admin.register(Climate)
class ClimateTemperatureAdmin(admin.ModelAdmin):
    # list_display = ("id", "year", "month", "latitude", "longitude", "mean_value", "created_at")
    list_filter = ("year", "month", "country_name", "country_code", "source")
    search_fields = ("latitude", "longitude", "country_name", "country_code")


    def get_list_display(self, request):
        """
        Dynamically show all fields in the admin list view
        """
        return [field.name for field in self.model._meta.fields]