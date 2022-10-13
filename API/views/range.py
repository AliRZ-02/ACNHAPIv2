from API import get_ranged_data_query, generate_output, Date
from API.views import SUCCESS, ERROR
from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/villagers/{trait}/{value1}/{value2}", status_code=SUCCESS, tags=["Villager Data Endpoints"])
async def return_creature_range_search(trait: str, value1: str, value2: str):
    try:
        data = await get_ranged_data_query("villagers", trait, value1, value2)
        date = Date(dateObj=datetime.today())
        params = {f"{trait}Start": f"{value1}", f"{trait}End": f"{value2}"}
        return generate_output("info", data, date, page_size=None, page=None, params=params)
    except Exception:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for creatures of type 'villagers' with trait '{trait}' and values between '{value1}' & '{value2}")

@router.get("/{type}/{trait}/{value1}-{value2}", status_code=SUCCESS, tags=["Creature Data Endpoints"])
async def return_creature_range_search(type: str, trait: str, value1: str, value2: str):
    try:
        data = await get_ranged_data_query(type, trait, value1, value2)
        date = Date(dateObj=datetime.today())
        params = {"type": type, f"{trait}": f"{value1}-{value2}"}
        return generate_output("info", data, date, page_size=None, page=None, params=params)
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for creatures of type '{type}' with trait '{trait}' and values between '{value1}' & '{value2}")
