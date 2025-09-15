from django.urls import path, include
from .open_meteo.views import DailyWeatherView, MonthlyWeatherView

urlpatterns = [
    path("open-meto/", include([
        path("daily", DailyWeatherView.as_view(), name="weather_daily"),
        path("monthly", MonthlyWeatherView.as_view(), name="weather_monthly"),
        ])
    ),
]