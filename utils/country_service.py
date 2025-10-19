import os

from dotenv import load_dotenv

from utils.api_client import APIClient
from utils.constants import Constants
#
load_dotenv()
api_key = os.getenv("GEOAPIFY_API_KEY", "NO_API_KEY_PROVIDED")
#
# climate_client = APIClient(
#     api_key = token,
#     api_key_header = "token",
#     base_url=Constants.NATIONAL_CENTER_FOR_ENVIRONMENT_INFORAMTION_BASE_URL
#     )

geoapify_api_client = APIClient(base_url=Constants.GEOAPIFY_BASE_URL)
big_datacloud_api_client = APIClient(base_url=Constants.BIG_DATA_CLOUD_BASE_URL)

"""
API URL: https://api.geoapify.com/v1/geocode/reverse?lat={LAT}&lon={LON}&apiKey={YOUR_KEY}
"""
def get_country_details_1(lat, lon):
    endpoint = "/v1/geocode/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "apiKey": api_key
    }
    return geoapify_api_client.get(endpoint, params=params)

"""
API URL: https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={LAT}&longitude={LON}&localityLanguage=en
"""
def get_country_details(lat, lon):
    endpoint = "/data/reverse-geocode-client"
    params = {
        "latitude": lat,
        "longitude": lon,
        "localityLanguage": "en"
    }
    return big_datacloud_api_client.get(endpoint, params=params)