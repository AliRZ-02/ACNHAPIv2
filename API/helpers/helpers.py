from re import findall
from aiohttp import ClientSession
from datetime import datetime, timedelta
from typing import Any, Coroutine, Dict, Iterable, List

from API.structures import Date
from API.helpers.constants import ACNH_TWEET_DATA, ACNH_NAMES_DATA, ACNH_VILLAGER_DATA, ACNH_CREATURE_DATA, NORTH, SOUTH, JOINING, LEAVING
from API.helpers.acnhtweetapi import generate_tweet, generate_names_data
from API.helpers.request import SearchInput, ACNHTweetSearch, ACNHNameSearch, ACNHVillagerDataSearch, ACNHCreatureDataSearch

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Output + Metadata Generation
def generate_output(type: str, data: Iterable, date: Date, page_size: int = None, page: int = None, params: Dict[str, Any] = None):
    return {
        "queryInfo": {
            "type": type,
            "page": 1 if page is None else page,
            "page_size": len(data),
            "params": params,
            "date": date.as_dict()
        },
        "data": data
    }

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Computation Functions
def get_date_from_id(id: int) -> datetime:
    return datetime(2020, 1, 1) + timedelta(id - 1)

def get_list_of_pages(page_size: int, page: int, to_search: List[Any]):
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return to_search[start_idx:end_idx]

def get_tweet_data_tuple(group, date: Date):
    mode = JOINING if 1 == date.date else LEAVING
    hemisphere = NORTH if "North" in group else SOUTH
    hemisphereString = "North" if hemisphere == NORTH else "South"
    return (mode, hemisphere, hemisphereString)

async def ranged_trait_search(type: str, page_size: int, page: int, search_fn: Coroutine):
    data = []
    async with ClientSession() as session:
        to_search = get_list_of_pages(page_size, page, await search_fn())
        for id in to_search:
            data.append(await generate_names_data(session, SearchInput(type, id)))
    
    return data

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Filter Functions

def get_filter_fn(type: str):
    return {"bugs": isBug, "fish": isFish, "sea": isSea, "villagers": isVillager}[type]

def isVillager(tweet: str):
    return ("Joining us this month" not in tweet) and ("Leaving us this month" not in tweet)

def isSea(tweet: str):
    return ("Joining us this month are" in tweet) or ("Leaving us this month are" in tweet)

def isFish(tweet: str):
    return "shadow" in tweet and not isVillager(tweet) and not isSea(tweet)

def isBug(tweet: str):
    return not isVillager(tweet) and not isSea(tweet) and not isFish(tweet)

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Return Range Search Queries

async def range_search_villagers(value1: str, value2: str):
    data = []
    start = findall(r'\d{1,2}', value1)
    end = findall(r'\d{1,2}', value2)
    start_month, start_day = int(start[0]), int(start[1])
    end_month, end_day = int(end[0]), int(end[1])
    diff = (datetime(2020, end_month, end_day) - datetime(2020, start_month, start_day)).days
    
    assert diff >= 0

    for i in range(0, diff):
        async with ClientSession() as session:
            to_search = await ACNHTweetSearch(ACNH_TWEET_DATA, Date(dateObj=datetime(2020, start_month, start_day) + timedelta(days=i))).get_data()

            for id in to_search["villagers"]:
                data.append(await generate_names_data(session, SearchInput("villagers", id)))
    
    return data

async def range_search_time(type: str, trait: str, value1: str, value2: str):
    data = []
    async with ClientSession() as session:
        to_search = []
        for i in range(int(value1), int(value2)):
            to_search.extend(await ACNHCreatureDataSearch(ACNH_CREATURE_DATA, type, trait, str(i)).get_data())
            
        for id in set(to_search):
            data.append(await generate_names_data(session, SearchInput(type, f"{id}")))
    
    return data

async def range_search_price(type: str, trait: str, value1: str, value2: str):
    data = []
    all_trait_data = await ACNHCreatureDataSearch(ACNH_CREATURE_DATA, type, trait, value1).get_all_from_trait()
    to_search = [value for key, value in all_trait_data.items() if int(key) >= int(value1) and int(key) <= int(value2)]
    
    async with ClientSession() as session:
        for ids in to_search:
            for id in ids:
                data.append(await generate_names_data(session, SearchInput(type, f"{id}")))
    
    return data

async def get_ranged_data_query(type: str, trait: str, value1: str, value2: str):
    """Function to query data in a ranged manner"""

    data = []
    if type == "villagers":
        if trait == "birthday":
            data.extend(await range_search_villagers(value1, value2))
        else:
            raise Exception
    else:
        if trait == "time" or trait == "monthsNorth" or trait == "monthsSouth":
            data.extend(await range_search_time(type, trait, value1, value2))
        elif trait == "price" or trait == "price_flick" or trait == "price_cj":
            data.extend(await range_search_price(type, trait, value1, value2))
        else:
            raise Exception

    return data

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Return Creature Data
async def get_creatures_by_trait(type: str, trait: str, value: str, page_size: int, page: int):
    return await ranged_trait_search(type, page_size, page, ACNHCreatureDataSearch(ACNH_CREATURE_DATA, type, trait, value).get_data)

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Return Villager Data
async def get_villagers_by_trait(trait: str, value: str, page_size: int, page: int):
    return await ranged_trait_search("villagers", page_size, page, ACNHVillagerDataSearch(ACNH_VILLAGER_DATA, trait, value).get_data)

async def get_villagers_by_birthday(month: int, day: int):
    data = []

    async with ClientSession() as session:
        to_search = await ACNHTweetSearch(ACNH_TWEET_DATA, Date(year=2020, month=month, date=day)).get_data()
        for type, ids in to_search.items():
            if (type == "villagers"):
                for id in ids:
                    data.append(await generate_names_data(session, SearchInput("villagers", id)))
    
    return data

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Return Data by name
async def get_data_by_name(name: str, type: str):
    name = name.replace('-', ' ')
    name = name.title() if type == "villagers" else name

    async with ClientSession() as session:
        to_search = await ACNHNameSearch(ACNH_NAMES_DATA, name, type).get_data()
        return await generate_names_data(session, SearchInput(type, to_search))

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Return Tweet Data
async def get_tweets(date: Date, hemispheresWanted=None) -> List[str]:
    if hemispheresWanted is None:
        hemispheresWanted = [NORTH, SOUTH]

    tweets = []

    async with ClientSession() as session:
        to_search = await ACNHTweetSearch(ACNH_TWEET_DATA, date).get_data()
        for group, ids in to_search.items():
            mode, hemisphere, hemisphereString = get_tweet_data_tuple(group, date)
            for id in ids:
                if hemisphere in hemispheresWanted:
                    tweets.append(await generate_tweet(session, SearchInput(group.replace(hemisphereString, ''), id), date.month, hemisphere, mode))
    
    return tweets