from API.structures.CreatureData import CreatureData
from API.helpers.request.request import SearchInput
from API.helpers.constants import LEAVING
from typing import Any, Dict, Optional, Tuple, Union
from aiohttp import ClientSession

class SeaCreatureData(CreatureData):
    speed: str
    shadow: str

    def __init__(self, session: ClientSession, data: SearchInput) -> None:
        super().__init__(session, data)
    
    def as_dict(self) -> Dict[str, Any]:
        """Method to return instance data as dictionary"""

        to_return = super().as_dict()
        to_return['speed'] = self.speed
        to_return['shadow'] = self.shadow
        return to_return

    async def initialize(self) -> Union[None, Dict[str, Any]]:
        """ASYNC --- Method to initialize instance data with API data"""

        input = await super().initialize()
        self.speed = input.get('speed', None)
        self.shadow = input.get('shadow', None)
    
    # Accessor Methods
    def get_name(self) -> str:
        name = super().name__()

        if name == "chambered nautilus":
            return "chambered nautili".title()
        elif name == "octopus":
            return "octopi".title()
        elif name == "umbrella octopus":
            return "umbrella octopi".title()
        elif name == "moon jellyfish":
            return name.title()
        else:
            return (name + "s").title()
    
    def get_nmonth(self) -> str:
        return "5-9" if super().name__() == "gigas giant clam" else super().get_nmonth()
    
    def get_smonth(self) -> str:
        return super().get_smonth()
    
    def speed__(self) -> str:
        return self.speed.lower()
    
    def shadow__(self) -> str:
        return self.shadow.lower()
    
    def get_speed(self) -> str:
        return "moderately fast" if self.speed__() == "medium" else self.speed__()
    
    def get_shadow(self) -> str:
        shadow = self.shadow__()

        if shadow == "medium":
            return "medium-sized"
        elif shadow == "smallest":
            return "tiny"
        elif shadow == "largest":
            return "huge"
        else:
            return shadow
    
    def generate_tweet(self, month: int, hemisphere: int, mode: int) -> Optional[Tuple[str, str]]:
        """Method to return instance data as a condensed tweet"""
        
        super().generate_tweet(month, hemisphere, mode)
        starter = f"{super().get_intention().replace('this month is the', 'this month are the')} {self.get_name()}!"

        if super().isLeaving() and mode == LEAVING:
            return (f"{starter} Remember to catch one if you haven't already! {super().add_tags()}", self.get_image_url("sea"))
        else:
            return (f"{starter} They are {self.get_speed()} creatures with a {self.get_shadow()} shadow. They can be found {super().get_time()} and can be sold for {super().get_price()} bells. {super().add_tags()}", self.get_image_url("sea"))