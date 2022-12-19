import os
from API import get_images_from_filename
from API.views import SUCCESS, ERROR
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/months/{month}/{hemisphere}")
async def get_months_images(month: int, hemisphere: str):
    hemisphere_id = {"North": 0, "South": 1}.get(hemisphere, 0)
    image_id = month + (hemisphere_id * 12)
    try:
        if month < 1 or month > 12:
            raise Exception()

        return get_images_from_filename(f"./API/static/Images/months/Image {image_id}.jpg")
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in returning image for month {month} in hemisphere {hemisphere}")

@router.get("/{creature}/{id}", status_code=SUCCESS)
async def get_creature_images(creature: str, id: int):
    try:
        return get_images_from_filename(f"./API/static/Images/{creature}/Image {id}.jpg")
    except:
        raise HTTPException(status_code=ERROR, detail=f"Error in returning image for {creature} with ID: {id}")