import httpx
import os
from dotenv import load_dotenv
from typing import Any, Dict, Optional

# Load .env file
load_dotenv()

# Renamed from GraphQLClient
class ApiClient:
    
    def __init__(self, base_url: Optional[str] = None):
        # Use provided base_url or get from env
        self.base_url = base_url or os.getenv("API_BASE_URL")
        if not self.base_url:
            raise ValueError("API base URL must be provided or set via API_BASE_URL environment variable.")
        # Initialize session with base_url
        self.session = httpx.AsyncClient(base_url=self.base_url)
        
    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Helper method for making requests."""
        try:
            response = await self.session.request(method, endpoint, **kwargs)
            response.raise_for_status() # Raise HTTPStatusError for bad responses (4xx or 5xx)
            # Handle cases where response might be empty (e.g., 204 No Content)
            if response.status_code == 204:
                return None 
            return response.json()
        except httpx.HTTPStatusError as e:
            # Log or handle specific HTTP errors
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise # Re-raise the exception after logging
        except httpx.RequestError as e:
            # Handle connection errors, timeouts, etc.
            print(f"Request error occurred: {e}")
            raise # Re-raise

    # Example methods for standard REST operations
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Any:
        return await self._request("POST", endpoint, data=data, json=json)

    async def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Any:
        return await self._request("PUT", endpoint, data=data, json=json)

    async def delete(self, endpoint: str) -> Any:
        return await self._request("DELETE", endpoint)
    
    async def close(self):
        await self.session.aclose()
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close() 