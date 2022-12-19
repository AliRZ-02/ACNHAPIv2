from API import get_creatures_by_trait, generate_output, Date
from API.views import SUCCESS, ERROR, DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

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