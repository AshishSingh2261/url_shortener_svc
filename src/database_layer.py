import logging
import time
from typing import Dict

from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel


class Collections(BaseModel):
    counter_collection: str = "counter"
    url_collection: str = "urls"


collections = Collections()


class AsyncDatabaseClient:
    def __init__(self):
        try:
            self.connection = AsyncIOMotorClient("mongodb://mongodb/")
        except Exception as e:
            raise Exception(
                f"Error while connecting to mongoDB async client: {repr(e)}"
            )

    async def collection_connect(self):
        try:
            self.database = self.connection["tinyurl_db"]
            self.collections: Dict[str, AgnosticCollection] = {}
            collection_names = await self.database.list_collection_names()
            print("debug", collection_names)
            for name in collection_names:
                print(name)
                self.collections[name] = self.database[name]
        except Exception as e:
            logging.fatal(f"DocumentDB Connection failed: {repr(e)} {str(e)}")
            raise e

    async def insert(self, record: dict, collection: str) -> None:
        try:
            created_at = int(time.time())
            record["created_at"] = created_at
            await self.collections[collection].insert_one(record)
        except Exception as e:
            logging.error(f"error while inserting: {repr(e)}")
            raise e

    async def update(
        self, key: str, identifier: str, record: dict, collection: str
    ) -> None:
        try:
            created_at = int(time.time())
            record["created_at"] = created_at
            self.collections[collection].update_one({key: identifier}, {"$set": record})
        except Exception as e:
            logging.error(f"error while inserting: {repr(e)}")
            raise e

    async def find(self, key: str, identifier: str, collection: str) -> None:
        try:
            record = (
                await self.collections[collection].find({key: identifier}).to_list(1)
            )
            if record:
                return record[0]
            else:
                return None
        except Exception as e:
            logging.error(f"error while find: {repr(e)}")
            raise e


async_database_client = AsyncDatabaseClient()
