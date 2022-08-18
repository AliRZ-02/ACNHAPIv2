from API.structures import BugData, FishData, SeaCreatureData, VillagerData, SearchOutput
from API.helpers.request.request import SearchInput
from aiohttp import ClientSession
from fastapi import HTTPException

def get_output_object(session: ClientSession, data: SearchInput) -> SearchOutput:
    """Function to return an instance of an object based on the type of data we want to collect"""

    if data.endpoint == "bugs":
        return BugData(session, data)
    elif data.endpoint == "fish":
        return FishData(session, data)
    elif data.endpoint == "sea":
        return SeaCreatureData(session, data)
    elif data.endpoint == "villagers":
        return VillagerData(session, data)
    else:
        raise HTTPException(status_code=404, detail=f"No endpoint '{data.endpoint}' exists")

async def generate_names_data(session: ClientSession, data: SearchInput) -> str:
    """ASYNC --- Function to return the data collected as a dictionary"""

    output = get_output_object(session, data)

    await output.initialize()
    return output.as_dict()

async def generate_tweet(session: ClientSession, data: SearchInput, month: int, hemisphere: int, mode: int) -> str:
    """ASYNC --- Function to condense the data collected into a tweet"""
    
    output = get_output_object(session, data)

    await output.initialize()
    return output.generate_tweet(month, hemisphere, mode)
