from API.helpers.request.request import SearchInput
from typing import Any, Dict, Optional, Tuple, Union
from aiohttp import ClientSession

# Parent Class for Data Output
class SearchOutput:
    def __init__(self, session: ClientSession, data: SearchInput) -> None:
        self.session: ClientSession = session
        self.data: SearchInput = data
    
    async def initialize(self) -> Union[None, Dict[str, Any]]:
        """ASYNC --- Method to return API data requested"""

        return await self.data.get_data_request(self.session)
    
    def generate_tweet(self, month: int, hemisphere: int, mode: int) -> Optional[Tuple[str, str]]:
        """Method to set instance data that is used for tweets"""

        self.month: int = month
        self.hemisphere: int = hemisphere
        self.mode: int = mode
    
    def as_dict(self) -> Dict[str, Any]:
        """Method to return metadata for instance"""

        return {
            "endpoint_searched": self.data.endpoint,
            "id_searched": self.data.params
        }
    
    def add_tags(self) -> str:
        """Method to add hashtags to a tweet"""

        return "#AnimalCrossing #NewHorizons"

    def get_image_url(self, url_type: str) -> str:
        return f"/images/{url_type}/{self.id}"