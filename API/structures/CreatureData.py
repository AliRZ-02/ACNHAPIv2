from API.structures.AvailabilityData import AvailabilityData
from API.structures.SearchOutput import SearchOutput
from API.helpers.constants import LEAVING, JOINING, NORTH
from API.structures.NameData import NameData
from API.helpers.request.request import SearchInput
from typing import Any, Dict, List, Optional, Union
from aiohttp import ClientSession

class CreatureData(SearchOutput):
    id: Optional[int]
    file_name: Optional[str]
    name: Optional[NameData]
    availability: Optional[AvailabilityData]
    price: Optional[int]
    catch_phrase: Optional[str]
    museum_phrase: Optional[str]
    image_uri: Optional[str]
    icon_uri: Optional[str]

    def __init__(self, session: ClientSession, data: SearchInput) -> None:
        super().__init__(session, data)
        self.name = NameData()
        self.availability = AvailabilityData()
    
    def as_dict(self) -> Dict[str, Any]:
        """Method to return instance data as a dictionary"""

        return {
            "id": self.id,
            "file_name": self.file_name,
            "name": self.name.as_dict(),
            "availability": self.availability.as_dict(),
            "price": self.price,
            "catch_phrase": self.catch_phrase,
            "museum_phrase": self.museum_phrase,
            "image_uri": self.image_uri,
            "icon_uri": self.icon_uri
        }
    
    async def initialize(self) -> Union[None, Dict[str, Any]]:
        """Method to initialize instance data with API data"""

        input = await super().initialize()
        self.id = input.get("id", None)
        self.file_name = input.get("file-name", None)

        self.name.USen = input.get('name').get('name-USen', None)
        self.name.EUen = input.get('name').get('name-EUen', None)
        self.name.EUde = input.get('name').get('name-EUde', None)
        self.name.EUes = input.get('name').get('name-EUes', None)
        self.name.USes = input.get('name').get('name-USes', None)
        self.name.EUfr = input.get('name').get('name-EUfr', None)
        self.name.USfr = input.get('name').get('name-USfr', None)
        self.name.EUit = input.get('name').get('name-EUit', None)
        self.name.EUnl = input.get('name').get('name-EUnl', None)
        self.name.CNzh = input.get('name').get('name-CNzh', None)
        self.name.TWzh = input.get('name').get('name-TWzh', None)
        self.name.JPja = input.get('name').get('name-JPja', None)
        self.name.KRko = input.get('name').get('name-KRko', None)
        self.name.EUru = input.get('name').get('name-EUru', None)

        self.availability.month_northern = input.get("availability").get("month-northern", None)
        self.availability.month_southern = input.get("availability").get("month-southern", None)
        self.availability.time = input.get("availability").get("time", None)
        self.availability.isAllDay = input.get("availability").get("isAllDay", None)
        self.availability.location = input.get("availability").get("location", None)
        self.availability.rarity = input.get("availability").get("rarity", None)
        self.availability.month_array_northern = input.get("availability").get("month-array-northern", None)
        self.availability.month_array_southern = input.get("availability").get("month-array-southern", None)
        self.availability.time_array = input.get("availability").get("time-array", None)

        self.price = input.get('price', None)
        self.catch_phrase = input.get('catch-phrase', None)
        self.museum_phrase = input.get("museum-phrase", None)
        self.image_uri = input.get('image_uri', None)
        self.icon_uri = input.get("icon_uri", None)

        return input
    
    # Accessor Methods
    def name__(self) -> str:
        return self.name.USen.lower().strip()
    
    def rarity__(self) -> str:
        return self.availability.rarity

    def nmonth__(self) -> str:
        return self.availability.month_northern
    
    def nmonth_arr__(self) -> List[int]:
        return self.availability.month_array_northern
    
    def smonth__(self) -> str:
        return self.availability.month_southern
    
    def smonth_arr__(self) -> List[int]:
        return self.availability.month_array_southern
    
    def time__(self) -> str:
        return self.availability.time
    
    def location__(self) -> str:
        return self.availability.location
    
    def price__(self) -> int:
        return self.price
    
    # Methods to return data in modified form for tweets
    def get_name(self) -> str:
        return self.name__().title()
    
    def get_rarity(self) -> str:
        return self.rarity__()
    
    def get_nmonth(self) -> str:
        return "0-0" if self.nmonth__() == "" else self.nmonth__()
    
    def get_smonth(self) -> str:
        return "0-0" if self.smonth__() == "" else self.smonth__()
    
    def get_time(self) -> str:
        return "at all times" if self.time__() == "" else f"from {self.time__().lower().replace('-', 'to')}"
    
    def get_location(self) -> str:
        return self.location__().lower()
    
    def get_price(self) -> str:
        return f'{self.price__()}'
    
    # Helper Functions
    def isLeaving(self) -> bool:
        present = self.isPresent()
        nextMonth = ((self.month + 1) % 12) if self.month != 11 else 12
        return present and nextMonth not in self.nmonth_arr__() if self.hemisphere == NORTH else present and nextMonth not in self.smonth_arr__()
    
    def isJoining(self) -> bool:
        present = self.isPresent()
        prevMonth = ((self.month - 1) % 12) if self.month != 1 else 12
        return present and prevMonth not in self.nmonth_arr__() if self.hemisphere == NORTH else present and prevMonth not in self.smonth_arr__()
    
    def isPresent(self) -> bool:
        return self.month in self.nmonth_arr__() if self.hemisphere == NORTH else self.month in self.smonth_arr__()
    
    def get_intention(self) -> str:
        if self.isLeaving() and self.mode == LEAVING:
            return "Leaving us after this month is the"
        elif self.isJoining() and self.mode == JOINING:
            return "Joining us this month is the"
        else:
            return "N/A"