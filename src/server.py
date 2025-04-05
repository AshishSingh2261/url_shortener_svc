import asyncio
import logging

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.database_layer import async_database_client
from src.tinyurl import TinyUrl

app = FastAPI(
    title="TinyURL SVC",
    description="TinyURL Service",
    redirect_slashes=False,
    openapi_url="/service/api/v1/openapi.json",
    docs_url="/service/docs",
    redoc_url="/service/redoc",
)


class TinyUrlResponse(BaseModel):
    tiny_url: str
    original_url: str


class TinyUrlRequest(BaseModel):
    original_url: str


router = APIRouter(redirect_slashes=False)

tinyurl = TinyUrl()


@app.on_event("startup")
async def initiate_all_schedulers():
    database_connection_task = asyncio.create_task(
        async_database_client.collection_connect()
    )
    await database_connection_task
    create_counter_task = asyncio.create_task(tinyurl.create_new_counter())
    await create_counter_task


@router.post("/create_tiny_url")
async def create_tiny_url(t: TinyUrlRequest) -> TinyUrlResponse:
    """This function will create a tiny url and return the tiny url in response"""
    try:
        tiny_url = await tinyurl.build_tiny_url(t.original_url)

        tiny_url_result = TinyUrlResponse.model_validate(
            {"tiny_url": tiny_url, "original_url": t.original_url}
        )

        return tiny_url_result
    except Exception as e:
        logging.error(f"create tiny url api failed: {repr(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/fetch_original_url/{tiny_url_hash}")
async def fetch_tiny_url(tiny_url_hash: str):
    try:
        tiny_url = "https://tinyurl/" + tiny_url_hash
        original_url = await tinyurl.fetch_original_url(tiny_url)
        if original_url:
            return RedirectResponse(original_url)
        else:
            raise HTTPException(status_code=404, detail="Url Not Found")
    except Exception as e:
        logging.error(f"fetch tiny url api failed: {repr(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


app.include_router(router, prefix="/service")


if __name__:
    pass

# Done:
# 1. created a basic working model with mongodb and redis setup and redirect logic working.
# 2. Logging and exception chaining setup properly
# 3. DB writes and reads are optimised. Caching is implemented for reads
# 4. Type hints are added properly
# 5. Only load testing left
