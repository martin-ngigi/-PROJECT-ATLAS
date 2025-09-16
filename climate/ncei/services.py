from utils.api_client import APIClient
from utils.constants import Constants
import pandas as pd
import os
from dotenv import load_dotenv

""""
API Client for fetching weather data from the National Centers for Environmental Information (NCEI).
Sample URL: https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&startdate=2024-01-01&enddate=2024-12-31&limit=1000&bbox=1.8,40.0,1.7,40.1
"""

load_dotenv()
token = os.getenv("NATIONAL_CENTER_FOR_ENVIRONMENT_INFORAMTION_API_KEY", "NO_TOKEN_PROVIDED")

climate_client = APIClient(
    api_key = token,
    api_key_header = "token",
    base_url=Constants.NATIONAL_CENTER_FOR_ENVIRONMENT_INFORAMTION_BASE_URL
    )

def get_daily_weather(datasetid, datatypeid1, datatypeid2, startdate, enddate, bbox, limit=1000):
    endpoint = "cdo-web/api/v2/data"
    params = {
        "datasetid": datasetid,
        "datatypeid": datatypeid1,
        "datatypeid": datatypeid2,
        "startdate": startdate,
        "enddate": enddate,
        # "limit": limit,
        "bbox": bbox,
    }
    return climate_client.get(endpoint, params=params)

def get_monthly_avg_temperature(datasetid, datatypeid1, datatypeid2, startdate, enddate, bbox, limit=1000):
    endpoint = "cdo-web/api/v2/data"
    params = {
        "datasetid": datasetid,
        "datatypeid": datatypeid1,
        "datatypeid": datatypeid2,
        "startdate": startdate,
        "enddate": enddate,
        "limit": limit,
        "bbox": bbox,
    }
    data = climate_client.get(endpoint, params=params)

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data=data["results"])
    df["date"] = pd.to_datetime(df["date"])

    # Extract all unique years in the dataset
    unique_years = df["date"].dt.year.unique()

    #dictionary tot hold results for each year
    yearly_monthly_means = {}

    for year in unique_years:
        #Filter data for this year
        df_year = df[df["date"].dt.year == year]
        #Create year-month column
        df_year["year_month"] = df_year["date"].dt.strftime("%Y-%m")
        #Calculate monthly means
        monthly_means = df_year.groupby("year_month")["value"].mean()
        yearly_monthly_means[year] = monthly_means.to_dict()

    #Convert keys recursively to strings(if needed) before returning
    def convert_key_to_str(d):
        if isinstance(d, dict):
            return {str(k): convert_key_to_str(v) for k, v in d.items()}
        else:
            return d

    return convert_key_to_str(yearly_monthly_means)