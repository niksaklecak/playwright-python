import requests
import os
from dotenv import load_dotenv
from typing import Any, Dict, Optional
from urllib.parse import urljoin

# Load .env file
load_dotenv()

class ApiClient:
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("API_BASE_URL")
        if not self.base_url:
            raise ValueError("API base URL must be provided or set via API_BASE_URL environment variable.")
        # Use requests.Session
        self.session = requests.Session()
        
    # Make methods synchronous (remove async/await)
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Helper method for making requests."""
        # Construct full URL
        full_url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, full_url, **kwargs)
            response.raise_for_status() 
            if response.status_code == 204:
                return None 
            # Handle potential JSON decode error if response is not JSON
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return response.text # Return text if not JSON
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Any:
        return self._request("POST", endpoint, data=data, json=json)

    def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Any:
        return self._request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint: str) -> Any:
        return self._request("DELETE", endpoint)
    
    def close(self):
        self.session.close() # Use standard close
        
        # Close the session
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 