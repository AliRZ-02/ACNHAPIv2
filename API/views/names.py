from API import get_data_by_name, generate_output, Date
from fastapi import APIRouter, HTTPException
from API.views import SUCCESS, ERROR
from datetime import datetime

router = APIRouter()

@router.get("/{type}/{name}", status_code=SUCCESS)
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