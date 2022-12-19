from API.views import tweets, range, villagers, traits, images
from API import DESCRIPTION, TAGS_METADATA
from fastapi.responses import FileResponse
from fastapi import FastAPI

# Server Object
server = FastAPI(
    title="ACNHAPIv2",
    description=DESCRIPTION,
    version="2.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://github.com/AliRZ-02/ACNHAPIv2/blob/main/LICENSE"
    },
    openapi_tags=TAGS_METADATA,
    redoc_url="/",
    docs_url=None
)

favicon_path = './API/static/Images/misc/BotProfilePicture.png'

@server.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

server.include_router(images.router, prefix="/images", tags=["Image Endpoints"])
server.include_router(villagers.router, prefix="/villagers", tags=["Villager Data Endpoints"])
server.include_router(tweets.router, prefix="/tweets", tags=["Tweet Endpoints"])
server.include_router(range.router, prefix="/range")
server.include_router(traits.router)