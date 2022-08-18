from API.structures.CreatureData import CreatureData
from API.helpers.request.request import SearchInput
from API.helpers.constants import LEAVING
from typing import Any, Dict, Optional, Union
from aiohttp import ClientSession
from re import findall

class FishData(CreatureData):
    price_cj: Optional[int]
    shadow: str

    def __init__(self, session: ClientSession, data: SearchInput) -> None:
        super().__init__(session, data)
    
    def as_dict(self) -> Dict[str, Any]:
        """Method to return instance data as dictionary"""

        to_return = super().as_dict()
        to_return['price_cj'] = self.price_cj
        to_return['shadow'] = self.shadow
        return to_return

    async def initialize(self) -> Union[None, Dict[str, Any]]:
        """ASYNC --- Method to initialize instance with data"""

        input = await super().initialize()
        self.price_cj = input.get('price-cj', None)
        self.shadow = input.get('shadow', None)
        self.shadow_arr = ["narrow", "tiny", "small", "medium-sized", "medium-sized", "large", "huge"]
    
    # Accessor Methods
    def shadow__(self) -> int:
        sizeElements = findall(r'\d', self.shadow)
        return int(sizeElements[0]) if len(sizeElements) != 0 else 0
    
    # Methods to return modified instance data for tweets
    def hasFin(self) -> bool:
        return len(findall(r'\sfin\s', self.shadow)) != 0
    
    def get_shadow(self) -> str:
        shadow_size = self.shadow__()
        return f'{self.shadow_arr[shadow_size]} shadow with a fin' if self.hasFin() else f'{self.shadow_arr[shadow_size]} shadow'
    
    def get_nmonth(self) -> str:
        return "3-11" if super().name__() in ["barred knifejaw"] else super().get_nmonth()
    
    def get_smonth(self) -> str:
        return "10-5" if super().name__() in ["guppy", "neon tetra"] else super().get_smonth()
    
    def get_location(self) -> str:
        location = super().get_location()

        if location == "River (Clifftop) & Pond".lower():
            location = "clifftop rivers & in ponds"
        elif location == "River".lower():
            location = "rivers"
        elif location == "Pier".lower():
            location = "the water next to a pier"
        elif location == "Sea (when raining or snowing)".lower():
            location = "a rainy or snowy sea"
        elif location == "River (Mouth)".lower():
            location = "the mouth of a river"
        elif location == "River (Clifftop)".lower():
            location = "clifftop rivers"
        elif location == "Sea".lower():
            location = "the sea"
        elif location == "Pond".lower():
            location = "ponds"
        else:
            raise Exception()
        
        return f'in {location}'
    
    def generate_tweet(self, month: int, hemisphere: int, mode: int) -> Optional[str]:
        """Method to return instance data condensed into a tweet"""
        
        super().generate_tweet(month, hemisphere, mode)
        starter = f"{super().get_intention()} {super().get_name()}!"

        if super().isLeaving() and mode == LEAVING:
            return f"{starter} Remember to catch one if you haven't already! {super().add_tags()}"
        else:
            return f"{starter} It is {self.get_rarity()} and can be found {self.get_location()} {super().get_time()}. It can be sold for {super().get_price()} bells and it has a {self.get_shadow()}. {super().add_tags()}"


