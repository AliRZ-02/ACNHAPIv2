from API import get_data_by_name, get_creatures_by_trait, generate_output, Date
from API.views import SUCCESS, ERROR, DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/{type}/name/{name}", status_code=SUCCESS, tags=["Name Search Endpoints"])
async def return_data_by_name(type: str, name: str):
    """
    - Inputs:\n
        - type
            - One of ["bugs", "fish", "sea", "villagers"]
        - name
    
    - Outputs:\n
        - Data Output Object
    """
    try:
        if type.lower() in ["bugs", "fish", "sea", "villagers"]:
            data = await get_data_by_name(name, type)
            return generate_output("info", data, Date(dateObj=datetime.today()), page_size=None, page=None, params={"type": type, "name": name})
        else:
            raise Exception()
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for type '{type}' with name '{name}'")

@router.get("/{type}/{trait}/{value}", status_code=SUCCESS, tags=["Creature Data Endpoints"])
async def return_creatures_by_trait(type: str, trait: str, value: str, page_size: int = DEFAULT_PAGE_SIZE, page: int = DEFAULT_PAGE):
    """
    - Inputs:\n
        - type
            - One of ["bugs", "fish", "sea", "villagers"]
        - name
    
    - Outputs:\n
        - Data Output Object
    """
    try: 
        data = await get_creatures_by_trait(type, trait, value, page_size, page)
        date = Date(dateObj=datetime.today())
        return generate_output("info", data, date, page_size, page, params={"type": type, f"{trait}": value})
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in generating data for creatures of type '{type}' with trait '{trait}' and value '{value}'")