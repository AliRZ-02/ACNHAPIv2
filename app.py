from API import get_date_from_id, get_tweets, get_filter_fn, get_data_by_name, get_villagers_by_birthday, get_villagers_by_trait, get_ranged_data_query, get_creatures_by_trait, generate_output, Date
from fastapi import FastAPI, HTTPException
from datetime import datetime

# Constants
DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE = 1
MAX_DATE = 366
SUCCESS = 200
MIN_DATE = 1
ERROR = 404

# Server Object
server = FastAPI()

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Tweet Endpoints

@server.get("/tweets/today", status_code=SUCCESS)
async def return_tweets_today():
    try:
        today = Date(dateObj=datetime.today())
        return generate_output("tweets", await get_tweets(today), today)
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating today's tweets")

@server.get("/tweets/{id}", status_code=SUCCESS)
async def return_tweets_by_id(id: int):
    try:
        if int(id) <= MAX_DATE and int(id) >= MIN_DATE:
            date = Date(dateObj=get_date_from_id(int(id)))
            return generate_output("tweets", await get_tweets(date), date, page_size=None, page=None, params={"id": id})
        else:
            raise Exception()
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating tweets for day {id}")

@server.get("/tweets/{type}/{id}", status_code=SUCCESS)
async def return_tweets_by_type(type: str, id: str):
    try:
        if type.lower() in ["bugs", "fish", "sea", "villagers"]:
            date = Date(dateObj=get_date_from_id(int(id)))
            tweets = list(filter(get_filter_fn(type), await get_tweets(date)))
            return generate_output("tweets", tweets, date, page_size=None, page=None, params={"type": type, "id": id})
        else:
            raise Exception()
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating tweets for type '{type}' on day '{id}'")

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Search For [bugs, fish, seaCreatures, villagers] by name

@server.get("/{type}/name/{name}", status_code=SUCCESS)
async def return_data_by_name(type: str, name: str):
    try:
        if type.lower() in ["bugs", "fish", "sea", "villagers"]:
            data = await get_data_by_name(name, type)
            return generate_output("info", data, Date(dateObj=datetime.today()), page_size=None, page=None, params={"type": type, "name": name})
        else:
            raise Exception()
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for type '{type}' with name '{name}'")

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Search for [villagers] data

@server.get("/villagers/birthday/{month}-{day}", status_code=SUCCESS)
async def return_villagers_by_birthday(month: int, day: int):
    try:
        data = await get_villagers_by_birthday(month, day)
        date = Date(dateObj=datetime.today())
        return generate_output("info", data, date, page_size=None, page=None, params={"birthMonth": month, "birthDate": day})
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for date:'{month}-{day}'")

@server.get("/villagers/{trait}/{value}", status_code=SUCCESS)
async def return_villagers_by_trait(trait: str, value: str, page_size: int = DEFAULT_PAGE_SIZE, page: int = DEFAULT_PAGE):
    try:
        data = await get_villagers_by_trait(trait, value.title(), page_size, page)
        date = Date(dateObj=datetime.today())
        return generate_output("info", data, date, page_size, page, params={f"{trait}": value})
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for trait '{trait}' with value '{value}'")

@server.get("/range/villagers/{trait}/{value1}/{value2}", status_code=SUCCESS)
async def return_creature_range_search(trait: str, value1: str, value2: str):
    try:
        data = await get_ranged_data_query("villagers", trait, value1, value2)
        date = Date(dateObj=datetime.today())
        params = {f"{trait}Start": f"{value1}", f"{trait}End": f"{value2}"}
        return generate_output("info", data, date, page_size=None, page=None, params=params)
    except Exception:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for creatures of type 'villagers' with trait '{trait}' and values between '{value1}' & '{value2}")

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Search for [bugs, fish, seaCreatures] in range

@server.get("/range/{type}/{trait}/{value1}-{value2}", status_code=SUCCESS)
async def return_creature_range_search(type: str, trait: str, value1: str, value2: str):
    try:
        data = await get_ranged_data_query(type, trait, value1, value2)
        date = Date(dateObj=datetime.today())
        params = {"type": type, "{trait}": f"{value1}-{value2}"}
        return generate_output("info", data, date, page_size=None, page=None, params=params)
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for creatures of type '{type}' with trait '{trait}' and values between '{value1}' & '{value2}")

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Search for type in [bugs, fish, seaCreatures] with obj[trait] = value
@server.get("/{type}/{trait}/{value}", status_code=SUCCESS)
async def return_creatures_by_trait(type: str, trait: str, value: str, page_size: int = DEFAULT_PAGE_SIZE, page: int = DEFAULT_PAGE):
    try: 
        data = await get_creatures_by_trait(type, trait, value, page_size, page)
        date = Date(dateObj=datetime.today())
        return generate_output("info", data, date, page_size, page, params={"type": type, f"{trait}": value})
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for creatures of type '{type}' with trait '{trait}' and value '{value}'")