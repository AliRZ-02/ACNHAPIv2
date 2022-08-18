from API.helpers.request.request import ACNH_URL
from aiohttp import ClientSession
from re import findall
import asyncio
import json

# Helper Functions
def isEmpty(obj): 
    return obj is None or len(obj) == 0

def get_months():
    return {"1": 31, "2": 29, "3": 31, "4": 30, "5": 31, "6": 30, "7": 31, "8": 31, "9": 30, "10": 31, "11": 30, "12": 31}

def get_endpoint_limits():
    return {"bugs": 81, "fish": 81, "sea": 41, "villagers": 392}

def generate_data():
    data = {}
    months = get_months()

    for (month, days) in months.items():
        for date in range(1, days + 1):
            data[f"{month}/{date}"] = {
                "bugsNorth": [],
                "fishNorth": [],
                "seaNorth": [],
                "bugsSouth": [],
                "fishSouth": [],
                "seaSouth": [],
                "villagers": []
            }
    
    return data

def generate_name_data():
    return {
        "bugs": {},
        "fish": {},
        "sea": {},
        "villagers": {}
    }

def get_villager_characteristics():
    return {
        "personality": {},
        "species": {},
        "gender": {},
        "personality_and_subtype": {},
        "hobby": {}
    }

def get_creature_characteristics():
    return {
        "bugs": {
            "time": {},
            "location": {},
            "monthsNorth": {},
            "monthsSouth": {},
            "rarity": {},
            "price": {},
            "price_flick": {},
            "isAllDay": {},
            "isAllYear": {}
        },
        "fish": {
            "time": {},
            "location": {},
            "monthsNorth": {},
            "monthsSouth": {},
            "rarity": {},
            "price": {},
            "price_cj": {},
            "shadow": {},
            "isAllDay": {},
            "isAllYear": {}
        },
        "sea": {
            "time": {},
            "monthsNorth": {},
            "monthsSouth": {},
            "speed": {},
            "price": {},
            "shadow": {},
            "isAllDay": {},
            "isAllYear": {}
        }
    }

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Mapping All Creature Data to IDs
async def get_creature_data():
    limits = get_endpoint_limits()
    data = get_creature_characteristics()

    async with ClientSession() as session:
        for endpoint in ["bugs", "fish", "sea"]:
            for i in range(1, limits[endpoint]):
                async with session.get(f"{ACNH_URL}{endpoint}/{i}") as resp:
                    response = await resp.json()
                    availability = response["availability"]

                    isAllDay = availability["isAllDay"]
                    isAllYear = availability["isAllYear"]
                    monthsNorth = availability["month-array-northern"]
                    monthsSouth = availability["month-array-southern"]
                    time_arr = availability["time-array"]
                    price = response["price"]

                    for hr in time_arr:
                        if isEmpty(data[endpoint]["time"].get(f"{hr}")):
                            data[endpoint]["time"][f"{hr}"] = [i]
                        else:
                            data[endpoint]["time"][f"{hr}"].append(i)
                    
                    for month in monthsNorth:
                        if isEmpty(data[endpoint]["monthsNorth"].get(f"{month}")):
                            data[endpoint]["monthsNorth"][f"{month}"] = [i]
                        else:
                            data[endpoint]["monthsNorth"][f"{month}"].append(i)
                    
                    for month in monthsSouth:
                        if isEmpty(data[endpoint]["monthsSouth"].get(f"{month}")):
                            data[endpoint]["monthsSouth"][f"{month}"] = [i]
                        else:
                            data[endpoint]["monthsSouth"][f"{month}"].append(i)
                    
                    if isEmpty(data[endpoint]["isAllDay"].get(f"{isAllDay}")):
                        data[endpoint]["isAllDay"][f"{isAllDay}"] = [i]
                    else:
                        data[endpoint]["isAllDay"][f"{isAllDay}"].append(i)
                    
                    if isEmpty(data[endpoint]["isAllYear"].get(f"{isAllYear}")):
                        data[endpoint]["isAllYear"][f"{isAllYear}"] = [i]
                    else:
                        data[endpoint]["isAllYear"][f"{isAllYear}"].append(i)
                    
                    if isEmpty(data[endpoint]["price"].get(f"{price}")):
                        data[endpoint]["price"][f"{price}"] = [i]
                    else:
                        data[endpoint]["price"][f"{price}"].append(i)

                    if endpoint == "bugs":
                        location = availability["location"]
                        rarity = availability["rarity"]
                        price_flick = response["price-flick"]

                        if isEmpty(data[endpoint]["location"].get(location)):
                            data[endpoint]["location"][location] = [i]
                        else:
                            data[endpoint]["location"][location].append(i)
                        
                        if isEmpty(data[endpoint]["rarity"].get(rarity)):
                            data[endpoint]["rarity"][rarity] = [i]
                        else:
                            data[endpoint]["rarity"][rarity].append(i)
                        
                        if isEmpty(data[endpoint]["price_flick"].get(price_flick)):
                            data[endpoint]["price_flick"][price_flick] = [i]
                        else:
                            data[endpoint]["price_flick"][price_flick].append(i)
                    elif endpoint == "fish":
                        location = availability["location"]
                        rarity = availability["rarity"]
                        price_cj = response["price-cj"]
                        shadow = response["shadow"]

                        if isEmpty(data[endpoint]["location"].get(location)):
                            data[endpoint]["location"][location] = [i]
                        else:
                            data[endpoint]["location"][location].append(i)
                        
                        if isEmpty(data[endpoint]["rarity"].get(rarity)):
                            data[endpoint]["rarity"][rarity] = [i]
                        else:
                            data[endpoint]["rarity"][rarity].append(i)
                        
                        if isEmpty(data[endpoint]["price_cj"].get(price_cj)):
                            data[endpoint]["price_cj"][price_cj] = [i]
                        else:
                            data[endpoint]["price_cj"][price_cj].append(i)

                        if isEmpty(data[endpoint]["shadow"].get(shadow)):
                            data[endpoint]["shadow"][shadow] = [i]
                        else:
                            data[endpoint]["shadow"][shadow].append(i)
                    else:
                        speed = response["speed"]
                        shadow = response["shadow"]

                        if isEmpty(data[endpoint]["speed"].get(speed)):
                            data[endpoint]["speed"][speed] = [i]
                        else:
                            data[endpoint]["speed"][speed].append(i)

                        if isEmpty(data[endpoint]["shadow"].get(shadow)):
                            data[endpoint]["shadow"][shadow] = [i]
                        else:
                            data[endpoint]["shadow"][shadow].append(i)
    
    for endpoint in ["bugs", "fish", "sea"]:
        for k, _ in data[endpoint].items():
            try:
                data[endpoint][k] = dict(sorted(data[endpoint][k].items(), key=lambda x: int(x[0])))
            except:
                data[endpoint][k] = dict(sorted(data[endpoint][k].items()))

    return data

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Mapping all Villager Data to IDs
async def get_villager_data():
    limit = get_endpoint_limits()['villagers']
    data = get_villager_characteristics()

    async with ClientSession() as session:
        for i in range(1, limit):
            async with session.get(f"{ACNH_URL}villagers/{i}") as resp:
                response = await resp.json()
                personality = response['personality']
                species = response['species']
                gender = response['gender']
                subtype = response['subtype']
                hobby = response['hobby']
                
                if isEmpty(data["personality"].get(personality)): data["personality"][personality] = [i]
                else: data["personality"][personality].append(i)
                
                if isEmpty(data["species"].get(species)): data["species"][species] = [i]
                else: data["species"][species].append(i)

                if isEmpty(data["gender"].get(gender)): data["gender"][gender] = [i]
                else: data["gender"][gender].append(i)

                if isEmpty(data["personality_and_subtype"].get(f"{personality}-{subtype}")):
                    data["personality_and_subtype"][f"{personality}-{subtype}"] = [i]
                else: data["personality_and_subtype"][f"{personality}-{subtype}"].append(i)

                if isEmpty(data["hobby"].get(hobby)): data["hobby"][hobby] = [i]
                else: data["hobby"][hobby].append(i)
        
    return data

# -------------------------------------------------------------------------------------------------------------------------------------------------
# MApping All Names to IDs
async def get_names():
    data = generate_name_data()
    endpoint_limits = get_endpoint_limits()

    async with ClientSession() as session:
        for endpoint in ["bugs", "fish", "sea", "villagers"]:
            for params in range(1, endpoint_limits[endpoint]):
                async with session.get(f"{ACNH_URL}{endpoint}/{params}") as resp:
                    response = await resp.json()
                    data[endpoint][response['name']['name-USen']] = params
    
    return data

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Mapping All Days to Tweet IDs
async def get_info():
    data = generate_data()
    endpoint_limits = get_endpoint_limits()

    async with ClientSession() as session:
        for endpoint in ["bugs", "fish", "sea", "villagers"]:
            for params in range(1, endpoint_limits[endpoint]):
                async with session.get(f"{ACNH_URL}{endpoint}/{params}") as resp:
                    response = await resp.json()
                    if endpoint == "villagers":
                        dates = findall(r'\d{1,2}', response['birthday'])
                        data[f"{dates[1]}/{dates[0]}"][endpoint].append(params)
                    else:
                        for hemisphere in ["North", "South"]:
                            availability = response['availability'][f'month-{hemisphere.lower()}ern']
                            firstMonths = findall(r'\d{1,2}\-', availability)
                            lastMonths = findall(r'\-\d{1,2}', availability)
                            firstMonths = [int(month.replace('-', '')) for month in firstMonths]
                            lastMonths = [int(month.replace('-', '')) for month in lastMonths]

                            for month in firstMonths:
                                data[f"{month}/1"][f"{endpoint}{hemisphere}"].append(params)
                            
                            for month in lastMonths:
                                day = 22
                                if month in [1, 3, 5, 7, 8, 10, 12]:
                                    day = 25
                                elif month in [4, 6, 9, 11]:
                                    day = 24

                                data[f"{month}/{day}"][f"{endpoint}{hemisphere}"].append(params)
    
    return data