from API.structures.Date import Date
import aiofiles
import json

# Parent Class
class JSONSearch:
    fileName: str

    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
    
    async def get_data(self):
        """ASYNC --- Method to load JSON data from given file"""

        async with aiofiles.open(self.fileName, mode='r') as f:
            return json.loads(await f.read())

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Child Class to Access Creature Data
class ACNHCreatureDataSearch(JSONSearch):
    type: str
    trait: str
    value: str

    def __init__(self, fileName: str, type: str, trait: str, value: str) -> None:
        super().__init__(fileName)
        self.type = type
        self.trait = trait
        self.value = value
    
    async def get_data(self):
        """ASYNC --- Method to return IDs for creatures with the specifies type, trait and value"""

        file_data = await super().get_data()
        return file_data[self.type][self.trait][self.value]
    
    async def get_all_from_trait(self):
        """ASYNC --- Method to return a List of IDs for objects within the specified type and trait"""

        return (await super().get_data())[self.type][self.trait]

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Child Class to Access Villager Data
class ACNHVillagerDataSearch(JSONSearch):
    attribute: str
    value: str

    def __init__(self, fileName: str, attribute: str, value: str) -> None:
        super().__init__(fileName)
        self.attribute = attribute
        self.value = value
    
    async def get_data(self):
        """ASYNC --- Method to return Villagers with the specified attribute and corresponding value"""

        file_data = await super().get_data()
        return file_data[self.attribute][self.value]

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Child Class to Access Villagers and Creatures by names
class ACNHNameSearch(JSONSearch):
    name: str
    type: str

    def __init__(self, fileName: str, name: str = None, type: str = None) -> None:
        super().__init__(fileName)
        self.name = name
        self.type = type
    
    async def get_data(self):
        """ASYNC --- Method to return IDs by the specified type and name"""

        file_data = await super().get_data()
        return file_data[self.type][self.name]

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Child Class to Access Tweets by Date
class ACNHTweetSearch(JSONSearch):
    date: Date

    def __init__(self, fileName: str, date: Date = None) -> None:
        super().__init__(fileName)
        self.date = date
    
    async def get_data(self):
        """ASYNC --- Method to return all the tweets for a given date"""

        file_data = await super().get_data()
        return file_data[f"{self.date.month}/{self.date.date}"]
