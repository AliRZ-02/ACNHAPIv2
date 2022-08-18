from typing import Any, Dict
import aiohttp

# Constants
ACNH_URL = "http://acnhapi.com/v1/"

# Exception Class
class RequestException(Exception):
    message: str

# SearchInput Class -> Used for Requesting Data from ACNH API
class SearchInput:
    endpoint: str
    params: str

    def __init__(self, endpoint, params) -> None:
        self.endpoint = endpoint
        self.params = params
    
    async def get_data_request(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """ASYNC --- Method to return data for a query to this instances' endpoint and param"""

        async with session.get(url=f'{ACNH_URL}{self.endpoint}/{self.params}') as response:
            dataJson = await response.json()
            dataJson["endpoint"], dataJson["params"] = self.endpoint, self.params
            return dataJson