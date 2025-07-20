from motor.motor_asyncio import AsyncIOMotorClient
from . import mongo
from app.core.config import settings

_client: AsyncIOMotorClient | None = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
    return _client


def get_db():
    client = get_client()
    return client[settings.MONGO_DB]