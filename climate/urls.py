from django.urls import path
from .views import DailyWeatherView, MonthlyWeatherView

urlpatterns = [
    path("weather/daily/", DailyWeatherView.as_view(), name="weather_daily"),
    path("weather/monthly/", MonthlyWeatherView.as_view(), name="weather_monthly"),

]