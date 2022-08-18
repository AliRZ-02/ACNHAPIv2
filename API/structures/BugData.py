from API.structures.CreatureData import CreatureData
from API.helpers.request.request import SearchInput
from typing import Any, Dict, Optional, Union
from API.helpers.constants import LEAVING
from aiohttp import ClientSession

class BugData(CreatureData):
    price_flick: Optional[int]

    def __init__(self, session: ClientSession, data: SearchInput) -> None:
        super().__init__(session, data)
    
    def as_dict(self) -> Dict[str, Any]:
        """Method to return Data as a Dictionary"""

        to_return = super().as_dict()
        to_return['price_flick'] = self.price_flick
        return to_return
    
    async def initialize(self) -> Union[None, Dict[str, Any]]:
        """ASYNC --- Method to get Data from ACNH API for data collection and initialize instance with values"""

        input = await super().initialize()
        self.price_flick = input.get('price-flick', None)

    def get_rarity(self) -> str:
        """Method to return rarity of the current bug instance"""

        return "rare" if (super().name__() == "tarantula" or super().name__() == "scorpion") else super().get_rarity().lower()
    
    def get_location(self) -> str:
        """Method to get the possible locations of the current bug instance"""

        location = super().get_location()

        if location == "hitting rocks": 
            return "by hitting rocks"
        elif location == "on rocks and bush (when raining)": 
            return "on rocks and bushes when it is raining"
        elif location == "shaking trees": 
            return "by shaking trees"
        elif location == "flying (near water)": 
            return "flying near water"
        else: 
            return location
    
    def get_nmonth(self) -> str:
        """Method to get the northern month availability data for current bug instance"""

        return "2-10" if super().name__() in ["tiger beetle"] else super().get_nmonth()
    
    def get_smonth(self) -> str:
        """Method to get the southern month availability data for current bug instance"""

        return "10-2" if super().name__() in ["common bluebottle", "jewel beetle"] else super().get_smonth()

    def generate_tweet(self, month: int, hemisphere: int, mode: int) -> Optional[str]:
        """Method to return a tweet string condensing the current bug instance's data"""

        super().generate_tweet(month, hemisphere, mode)
        starter = f"{super().get_intention()} {super().get_name()}!"

        if super().isLeaving() and mode == LEAVING:
            return f"{starter} Remember to catch one if you haven't already! {super().add_tags()}"
        else:
            return f"{starter} It is {self.get_rarity()} and can be found {self.get_location()} {super().get_time()}. It can be sold for {super().get_price()} bells. {super().add_tags()}"