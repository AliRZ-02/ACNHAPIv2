from API import get_villagers_by_birthday, get_villagers_by_trait, generate_output, Date
from API.views import SUCCESS, ERROR, DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/birthday/{month}-{day}", status_code=SUCCESS)
async def return_villagers_by_birthday(month: int, day: int):
    try:
        data = await get_villagers_by_birthday(month, day)
        date = Date(dateObj=datetime.today())
        return generate_output("info", data, date, page_size=None, page=None, params={"birthMonth": month, "birthDate": day})
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for date:'{month}-{day}'")

@router.get("/{trait}/{value}", status_code=SUCCESS)
async def return_villagers_by_trait(trait: str, value: str, page_size: int = DEFAULT_PAGE_SIZE, page: int = DEFAULT_PAGE):
    try:
        data = await get_villagers_by_trait(trait, value, page_size, page)
        date = Date(dateObj=datetime.today())
        return generate_output("info", data, date, page_size, page, params={f"{trait}": value})
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for trait '{trait}' with value '{value}'")