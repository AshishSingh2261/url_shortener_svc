import redis


class AsyncRedisClient:
    def __init__(
        self, host: str = "cache", port: int = 6379, db_number: int = 0
    ) -> None:
        self.counter_lock_expiry = 30
        self.host = host
        self.connection = redis.asyncio.Redis(host=self.host, port=port, db=db_number)

    def get_redis_connection(self) -> redis.asyncio.Redis:
        return self.connection

    async def get_counter_lock(self, counter_block_name):
        lock = self.connection.lock(
            counter_block_name, timeout=self.counter_lock_expiry
        )
        lock_acquired = await lock.acquire(blocking=False)

        return lock, lock_acquired

    async def release_counter_lock(self, counter_lock) -> None:
        await counter_lock.release()

    async def get(self, key: str) -> str:
        return await self.connection.get(key)

    async def set(self, key: str, value: str, expiry: int = 86400) -> None:
        await self.connection.set(key, value, ex=expiry)

    async def delete(self, key: str) -> None:
        await self.connection.delete(key)


async_redis_client = AsyncRedisClient()
