from utils.api_client import APIClient
from utils.constants import Constants
import pandas as pd

api_client = APIClient(base_url=Constants.NASA_BASE_URL)

"""
API URL: https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN&community=AG&longitude=1.7471&latitude=40.0573&start=20240101&end=20241231&format=JSON
"""
def get_monthly_temperature(parameters, community, latitude, longitude, start, end, format):
    endpoint = "/api/temporal/daily/point"
    params = {
        "parameters": parameters,
        "community": community,
        "latitude": latitude,
        "longitude": longitude,
        "end": end,
        "start": start,
        "format": format
    }
    return api_client.get(endpoint, params=params)

def get_monthly_avg_temperature(parameters, community, latitude, longitude, start, end, format):
    endpoint = "/api/temporal/daily/point"
    params = {
        "parameters": parameters,
        "community": community,
        "latitude": latitude,
        "longitude": longitude,
        "end": end,
        "start": start,
        "format": format
    }
    data =  api_client.get(endpoint, params=params)

    # Extract daily temperature data for paramete T2M
    daily_temps = data["properties"]["parameter"]["T2M"]

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(list(daily_temps.items()), columns=["date", "temperature"])
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df.set_index("date", inplace=True)

    # Calculate monthly average temperatures
    monthly_avg = df["temperature"].resample("M").mean()

    result = {}
    for date, temp in monthly_avg.items():
        year = str(date.year)
        month = date.strftime("%Y-%m")
        if year not in result:
            result[year] = {}
        result[year][month] = round(temp, 2)
    return result