from utils.api_client import APIClient
from utils.constants import Constants
import pandas as pd

climate_client = APIClient(base_url=Constants.OPEN_METO_BASE_URL)
archive_climate_client = APIClient(base_url=Constants.OPEN_METO_ARCHIVE_BASE_URL)

# hourly="temperature_2m,humidity_2m"
def get_daily_weather(latitude, longitude, start_date, end_date, daily):
    endpoint = "/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": daily,
        "timezone": "auto",
    }
    return archive_climate_client.get(endpoint, params=params)

def get_monthly_avg_temperature(latitude, longitude, start_date, end_date, daily):
    endpoint = "/v1/archive" 
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": daily,
        "timezone": "auto",
    }
    data =  archive_climate_client.get(endpoint, params=params)

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data=data["daily"])
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    # Resample to monthly frequency and calculate the mean
    monthly_avg = df["temperature_2m_mean"].resample("M").mean()

    #Group by year and create nested dictionary
    monthly_dict = {}
    for date, temp in monthly_avg.items():
        year = date.year
        month_str = date.strftime("%Y-%m")
        temp_rounded = round(temp, 2)
        if year not in monthly_dict:
            monthly_dict[year] = {}
        monthly_dict[year][month_str] = temp_rounded

    return monthly_dict