import traceback
from API import Date, generate_output, get_tweets, get_filter_fn, get_date_from_id, NORTH, SOUTH
from API.views import SUCCESS, ERROR, MIN_DATE, MAX_DATE
from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/today", status_code=SUCCESS)
async def return_tweets_today():
    """
    - Inputs:\n
        - **None**
    
    - Outputs:\n
        - Array of Tweets
    """
    try:
        today = Date(dateObj=datetime.today())
        data = await get_tweets(today)
        return generate_output("tweets", [{"tweet": item[0], "url": item[1]} for item in data], today)
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating today's tweets")

@router.get("/today/villagers", status_code=SUCCESS)
async def return_villager_tweets_today():
    """
    - Inputs:\n
        - **None**
    
    - Outputs:\n
        - Array of Tweets
            - Tweets for villagers only
    """
    try:
        today = Date(dateObj=datetime.today())
        data = list(filter(lambda x: get_filter_fn("villagers")(x[0]), await get_tweets(today)))
        return generate_output("tweets", [{"tweet": item[0], "url": item[1]} for item in data], today, page_size=None, page=None, params=None)
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating tweets for type '{type}' on day '{id}'")

@router.get("/today/{hemisphere}", status_code=SUCCESS)
async def return_hemisphere_tweets_today(hemisphere: str):
    """
    - Inputs:\n
        - hemisphere
            - One of ["North", "South"]
    
    - Outputs:\n
        - Array of Tweets 
            - Tweets for creatures in specified hemisphere only
    """
    hemispheresWanted = [NORTH] if hemisphere.lower().strip() == "north" else [SOUTH]
    try:
        fn = lambda tweet: not get_filter_fn("villagers")(tweet)
        today = Date(dateObj=datetime.today())
        data = list(filter(lambda x: fn(x[0]), await get_tweets(today, hemispheresWanted)))
        return generate_output("tweets", [{"tweet": item[0], "url": item[1]} for item in data], today)
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating today's tweets")

@router.get("/{id}", status_code=SUCCESS)
async def return_tweets_by_id(id: int):
    """
    - Inputs:\n
        - id
            - In range [1, 366]
    
    - Outputs:\n
        - Array of Tweets
            - Tweets for specified day of the year (including Feb. 29)
    """
    try:
        if int(id) <= MAX_DATE and int(id) >= MIN_DATE:
            date = Date(dateObj=get_date_from_id(int(id)))
            data = await get_tweets(date)
            return generate_output("tweets", [{"tweet": item[0], "url": item[1]} for item in data], date, page_size=None, page=None, params={"id": id})
        else:
            raise Exception()
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating tweets for day {id}")

@router.get("/{type}/{id}", status_code=SUCCESS)
async def return_tweets_by_type(type: str, id: str):
    """
    - Inputs:\n
        - type
            - One of ["bugs", "fish", "sea", "villagers"]
        - id
            - In range [1, 366]
    
    - Outputs:\n
        - Array of Tweets
            - Tweets of specified type for specified day of the year (including Feb. 29)
    """
    try:
        if type.lower() in ["bugs", "fish", "sea", "villagers"]:
            date = Date(dateObj=get_date_from_id(int(id)))
            tweets = list(filter(lambda x: get_filter_fn(type)(x[0]), await get_tweets(date)))
            return generate_output("tweets", [{"tweet": item[0], "url": item[1]} for item in tweets], date, page_size=None, page=None, params={"type": type, "id": id})
        else:
            raise Exception()
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating tweets for type '{type}' on day '{id}'")
