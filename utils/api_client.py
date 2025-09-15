import requests
from requests.exceptions import RequestException, Timeout, HTTPError
import logging

class APIClient:
    """
    Reusable API client for making HTTP requests across Djan apps. 
    Supports configurable API key headers, beare tokens and custom headers.
    """

    def __init__(
            self,
            base_url = None,
            api_key = None,
            api_key_header = "x-api-key",
            bearer_token = None,
            headers=None,
            timeout = 10,
            ):
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.timeout = timeout

        # defaults headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Default headers
        if headers:
            self.headers.update(headers)

        # API key auth (customizable header name)
        if api_key:
            self.headers[api_key_header] = api_key

        # Bearer token auth
        if bearer_token:
            self.headers["Authorization"] = f"Bearer {bearer_token}"

    def _build_url(self, endpoint):
        if self.base_url and not endpoint.startswith("http"):
            return f"{self.base_url}/{endpoint.lstrip('/')}"
        return endpoint
    
    def request(self, method, endpoint, params = None, data = None, json = None, headers = None):
        url = self._build_url(endpoint)
        try:
            response = requests.request(
                method = method.upper(),
                url = url,
                params = params,
                data = data,
                json = json,
                headers = {**self.headers, **(headers or {})},
                timeout = self.timeout
            )
            response.raise_for_status()
            logging.info(f"✅ SUCCESS: Request to {url} with status code {response.status_code}")
            return response.json()
        except Timeout:
            logging.error(f"❌ Request to {url} timed out.")
            raise Exception(f"Request to {url} timed out.")
        except HTTPError as http_err:
            logging.error(f"❌ Request to {url} timed out.")
            logging.error(f"HTTP error occurred: {http_err} - Response: {http_err.response.text}")
            raise Exception(f"HTTP error occurred: {http_err} - Response: {http_err.response.text}")
        except RequestException as req_err:
            logging.error(f"❌ Request to {url} timed out.")
            raise Exception(f"Request error occurred: {req_err}")
        except ValueError:
            logging.error(f"❌ Invalid JSON response from {url}")
            raise Exception(f"Invalid JSON response from {url}")
        except Exception as e:
            logging.error(f"❌ An error occurred: {e}")
            raise Exception(f"An error occurred: {e}")
        
    def get(self, endpoint, params = None, headers = None):
        return self.request("GET", endpoint = endpoint, params = params, headers = headers)
    
    def post(self, endpoint, data = None, json = None, headers = None):
        return self.request("POST", endpoint = endpoint, data = data, json = json, headers = headers)   
    
    def put(self, endpoint, data = None, json = None, headers = None):
        return self.request("PUT", endpoint = endpoint, data = data, json = json, headers = headers)

    def patch(self, endpoint, data = None, json = None, headers = None):
        return self.request("PATCH", endpoint = endpoint, data = data, json = json, headers = headers)
    
    def delete(self, endpoint, headers = None):
        return self.request("DELETE", endpoint = endpoint, headers = headers)
