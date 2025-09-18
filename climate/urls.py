from django.urls import path, include
from .open_meteo.views import DailyWeatherView, MonthlyWeatherView
from .ncei.views import NCEIDailyWeatherView, NCEIMonthlyWeatherView
from .nasa.views import NASADailyTemperatureView, NASAMonthlyTemperatureView
from .temp_views import AggregatedTemperatureView

urlpatterns = [
      path("temperature/", include([ 
          
          path("open-meto/", include([
              path("daily", DailyWeatherView.as_view(), name="weather_daily"),
              path("monthly", MonthlyWeatherView.as_view(), name="weather_monthly9"),
              ])),
              
            path("ncei/", include([
                path("daily", NCEIDailyWeatherView.as_view(), name="ncei_daily_weather"),
                path("monthly", NCEIMonthlyWeatherView.as_view(), name="ncei_monthly_weather"),
                ])),
                
            path("nasa/", include([
                path("daily", NASADailyTemperatureView.as_view(), name="nasa_daily_temperature"),
                path("monthly", NASAMonthlyTemperatureView.as_view(), name="nasa_monthly_temperature"),
                ])),

            path("aggregate/", include([
                path("monthly", AggregatedTemperatureView.as_view(), name="aggregate_monthly_temperature"),
                ])),


       ])),

]