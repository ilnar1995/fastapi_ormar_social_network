from typing import AsyncIterator
from src.config import REDIS_HOST
from aioredis import from_url, Redis


class DataConn:
    async def __aenter__(self):
        """
        Открываем подключение с redis.
        """
        self.session = from_url(f"redis://{REDIS_HOST}", encoding="utf-8", decode_responses=True)
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        """
        Закрываем подключение.
        """
        await self.session.close()


async def redis_session() -> AsyncIterator[Redis]:
    async with DataConn() as session:
        yield session
