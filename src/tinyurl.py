import asyncio
import logging

from src.database_layer import async_database_client, collections
from src.redis_client import async_redis_client

lock = asyncio.Lock()


class TinyUrl:
    def __init__(self) -> None:
        self.counter = None
        self.block_size = 10000
        self.counter_lock_name = "tinyurl_counter"
        # after multiplying this value by 10000, whenever we convert it to a base62 string,
        # we will get atleast 6 characters
        self.default_counter_block = 5680024

    async def build_tiny_url(self, original_url: str) -> str:
        async with lock:
            new_base_62_hash = await self.base_10_to_base_62(self.counter)
            self.counter += 1
        tinyurl = "https://tinyurl/" + new_base_62_hash

        tinyurl_record = {"original_url": original_url, "tiny_url": tinyurl}

        await async_database_client.insert(tinyurl_record, collections.url_collection)

        return tinyurl

    async def create_new_counter(self) -> None:
        """creates a new counter that starts from after the last used counter
        If no counter exists then creates a default one"""

        while True:
            counter_lock, if_lock_acquired = await async_redis_client.get_counter_lock(
                self.counter_lock_name
            )

            if if_lock_acquired:
                logging.info("Counter Lock Acquired")
                break

        counter_block = await async_database_client.find(
            "counter_block", "COUNTER_BLOCK", collections.counter_collection
        )

        if not counter_block:
            await self.create_new_counter_record()
        else:
            self.counter = (counter_block["current_block"] + 1) * self.block_size

            counter_block["current_block"] += 1

            await async_database_client.update(
                "counter_block",
                "COUNTER_BLOCK",
                counter_block,
                collections.counter_collection,
            )

        await async_redis_client.release_counter_lock(counter_lock)

        logging.info("Counter Lock Released")

    async def create_new_counter_record(self) -> None:
        """creates a new counter record in DB if one does not exist from a fixed block size"""

        default_record = {
            "counter_block": "COUNTER_BLOCK",
            "current_block": self.default_counter_block,
        }

        await async_database_client.insert(
            default_record, collections.counter_collection
        )

    async def base_10_to_base_62(self, deci: int) -> str:
        s = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        hash_str = ""
        while deci > 0:
            hash_str = s[(deci % 62)] + hash_str
            deci /= 62
            deci = int(deci)
        return hash_str

    async def fetch_original_url(self, tiny_url: str) -> str:
        """This will first try to fetch from cache, if missing it will look in DB and then insert to cache"""

        cache_record = await async_redis_client.get(tiny_url)

        if cache_record:
            cache_record = cache_record.decode("utf-8")
            return cache_record

        db_record = await async_database_client.find(
            "tiny_url", tiny_url, collections.url_collection
        )

        if db_record:
            original_url = db_record["original_url"]

            await async_redis_client.set(tiny_url, original_url)
            return original_url

        return None
